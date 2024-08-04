from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

import Database.database as db
import markups as mks

import generate_calendar
import datetime
import states
import config
import admin
import os


bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    db.db_start()


def get_formatted_date(date: str) -> str:
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message):
    db.create_profile(message.from_user.id, message.from_user.username)
    await message.reply(config.GREETINGS,
                        reply_markup=mks.main_menu)
    await states.Client.default.set()


@dp.message_handler(commands=['work'], state='*')
async def start_command(message: types.Message):
    if db.check_worker(message.from_user.id):
        await states.Worker.default.set()
        await message.answer('Меню работника', reply_markup=mks.worker_menu)


@dp.message_handler(commands=['admin'], state='*')
async def start_command(message: types.Message):
    if db.check_admin(message.from_user.id):
        await states.Admin.default.set()
        await message.answer('Меню админа', reply_markup=mks.admin_menu)


@dp.callback_query_handler(lambda c: c.data == 'add_worker', state=states.Admin.default)
async def add_worker(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id,
                           'Введите данные работника через пробел в формате: Username имя ссылка_на_работы')
    await states.Admin.info.set()


@dp.message_handler(state=states.Admin.info)
async def get_info(message: types.Message, state: FSMContext):
    info = message.text.split()
    await state.update_data(username=info[0], name=info[1], photos=info[2])
    await bot.send_message(message.from_user.id, 'Напишите описание')
    await states.Admin.description.set()


@dp.message_handler(state=states.Admin.description)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await states.Admin.default.set()
    await bot.send_message(message.from_user.id, 'Пришлите фото работника')


@dp.message_handler(content_types=['photo'], state=states.Admin.default)
async def get_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data['username']
    worker_id = db.find_worker(username)
    db.add_worker(worker_id, username, data['name'], data['photos'], data['description'])
    await message.photo[-1].download(f'photos/{username}_0.png')
    await bot.send_message(message.from_user.id, 'Работник успешно добавлен!')


@dp.callback_query_handler(lambda c: c.data == 'main_menu', state='*')
async def main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await states.Client.default.set()
    await callback_query.message.answer('🏠 Главное меню', reply_markup=mks.main_menu)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'show_adresses', state='*')
async def main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_photo(callback_query.from_user.id,
                         photo=types.InputFile('photos/address.png'),
                         caption=config.ADDRESS,
                         reply_markup=mks.to_menu_only)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'about_us', state='*')
async def main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_photo(callback_query.from_user.id,
                         photo=types.InputFile('photos/logo.png'),
                         caption=config.ABOUT_US,
                         reply_markup=mks.to_menu_only)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'to_workers', state='*')
async def choose_worker(callback_query: types.CallbackQuery, state: FSMContext):
    if not db.check_session(callback_query.from_user.id):
        await callback_query.message.answer(
            '🫂 Наши мастера готовы предоставить Вам лучший сервис и отменное качество! '
            'Вам остается только выбрать одного из наших профессионалов!')
        workers = db.get_workers()
        for worker in workers:
            caption = f'{worker[2]}\n\n' \
                      f'{worker[4]}\n\n' \
                      f'Работы: {worker[3]}'

            photo = types.InputFile(f'photos/{worker[1]}_0.png')

            keyboard = InlineKeyboardButton('Посмотреть записи', callback_data=f'worker_{worker[1]}')
            markup = InlineKeyboardMarkup(row_width=1).add(keyboard)

            await bot.send_photo(callback_query.from_user.id,
                                 photo=photo,
                                 caption=caption,
                                 parse_mode='HTML',
                                 reply_markup=markup)
    else:
        await callback_query.message.answer('У вас уже есть активная запись!', reply_markup=mks.to_menu_only)
    await callback_query.message.delete()



@dp.callback_query_handler(lambda c: c.data.startswith(('prev', 'next', 'day', 'time', 'off', 'cancel', 'worker')),
                           state='*')
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split('_')
    if data[0] == 'day':
        if int(data[1]) < 10:
            selected_day = f'0{str(data[1])}'
        else:
            selected_day = int(data[1])

        if int(data[2]) < 10:
            selected_month = f'0{str(data[2])}'
        else:
            selected_month = int(data[2])

        selected_year = int(data[3])
        date = f'{selected_year}-{selected_month}-{selected_day}'

        await state.update_data(date=date)

        data = await state.get_data()
        worker = data['worker']

        allowed_time = db.check_date(date, worker)

        if len(allowed_time) == 2:
            markup = InlineKeyboardMarkup()
            [markup.add(InlineKeyboardButton(text=allowed_time[i], callback_data=f'time_{allowed_time[i]}')) for i in
             range(2)]
            await callback_query.message.reply('Выберите время:', reply_markup=markup)
        else:
            await callback_query.message.reply('Нет свободных сеансов на эту дату')

    elif data[0] == 'prev' or data[0] == 'next':
        target_month = int(data[1])
        target_year = int(data[2])
        data = await state.get_data()
        worker = data['worker']
        await generate_calendar.show_calendar(callback_query.message, target_year, target_month, worker)

    elif data[0] == 'time':
        time = data[1]
        await state.update_data(time=time)
        data = await state.get_data()
        if db.check_user_info(callback_query.from_user.id):
            await callback_query.message.answer(f'Отлично!\n'
                                                f'Подтверждаете запись к @{data["worker"]} на '
                                                f'{get_formatted_date(data["date"])}?',
                                                reply_markup=mks.session_apply_markup)
        else:
            await states.Client.name.set()
            await callback_query.message.answer('Пожалуйста, введите Ваше имя:')

    elif data[0] == 'off':
        if int(data[1]) < 10:
            selected_day = f'0{str(data[1])}'
        else:
            selected_day = int(data[1])

        if int(data[2]) < 10:
            selected_month = f'0{str(data[2])}'
        else:
            selected_month = int(data[2])

        selected_year = int(data[3])
        date = f'{selected_year}-{selected_month}-{selected_day}'

        db.day_off(callback_query.from_user.username, date)
        await callback_query.message.answer(f'Вы назначили выходной на: \n{get_formatted_date(date)}')

    elif data[0] == 'cancel':
        await callback_query.message.answer(db.cancel_session(data[1]), reply_markup=mks.to_menu_only)

    elif data[0] == 'worker':
        await state.update_data(worker=data[1])
        current_date = datetime.datetime.now()
        await generate_calendar.show_calendar(callback_query.message, current_date.year, current_date.month, data[1])


@dp.message_handler(state=states.Client.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await states.Client.default.set()
    await state.update_data(name=name)
    await states.Client.number.set()
    await message.answer('Спасибо! Записали.\nТеперь введите, пожалуйста, Ваш номер телефона для связи:')


@dp.message_handler(state=states.Client.number)
async def get_number(message: types.Message, state: FSMContext):
    await states.Client.default.set()
    number = message.text

    await state.update_data(number=number)

    data = await state.get_data()

    db.add_user_info(message.from_user.id, data['name'], data['number'])

    await message.answer(f'Спасибо! Записали.\n'
                         f'Подтверждаете запись к @{data["worker"]} на {get_formatted_date(data["date"])}?',
                         reply_markup=mks.session_apply_markup)


@dp.callback_query_handler(lambda c: c.data == 'apply_session', state='*')
async def applied_session(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    answer = db.create_session(data['worker'], callback_query.from_user.id, data['date'], data['time'])
    await callback_query.message.answer(answer, reply_markup=mks.to_menu_only)
    worker_id = db.find_worker(data['worker'])
    await bot.send_message(worker_id,
                           f'У вас новая запись!\n@{callback_query.from_user.username}\n'
                           f'{get_formatted_date(data["date"])} {data["time"]}')


@dp.callback_query_handler(lambda c: c.data == 'show_sessions', state=states.Worker.default)
async def show_session(callback_query: types.CallbackQuery):
    sessions = db.get_incoming_sessions(callback_query.from_user.username)
    if sessions:
        await callback_query.message.answer(sessions, reply_markup=mks.to_menu_only)
    else:
        await callback_query.message.answer('У Вас нет записей на ближайшее время!', reply_markup=mks.to_menu_only)


@dp.callback_query_handler(lambda c: c.data == 'client_show_sessions', state='*')
async def client_show_session(callback_query: types.CallbackQuery):
    sessions = db.get_client_sessions(callback_query.from_user.id)
    if sessions:
        for session in sessions:
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отменить',
                                                                     callback_data=f'cancel_{session[0]}'))
            await callback_query.message.answer(f'Вы записаны на {get_formatted_date(session[2])} {session[3]} к мастеру @{session[1]}',
                                                reply_markup=markup)

    else:
        await callback_query.message.answer('У Вас нет записей на ближайшее время!', reply_markup=mks.to_menu_only)


@dp.callback_query_handler(lambda c: c.data == 'get_all_records', state=states.Admin.default)
async def get_all_records(callback_query: types.CallbackQuery):
    await admin.get_all_records(bot, callback_query.from_user.id)


@dp.callback_query_handler(lambda c: c.data == 'weekend', state=states.Worker.default)
async def weekend(callback_query: types.CallbackQuery, state: FSMContext):
    current_date = datetime.datetime.now()
    await state.update_data(worker=callback_query.from_user.username)
    await generate_calendar.show_calendar_for_day_off(callback_query.message,
                                                      current_date.year,
                                                      current_date.month,
                                                      callback_query.from_user.username)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp,
                           on_startup=on_startup,
                           skip_updates=True)
