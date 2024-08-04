from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import Database.database as db

import calendar
import datetime


def get_month(month):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
              "Декабрь"]
    return months[month-1]


def generate_calendar(year, month, worker):
    markup = InlineKeyboardMarkup(row_width=7)

    previous_month = datetime.datetime(year, month, 1) - datetime.timedelta(days=1)
    markup.insert(InlineKeyboardButton(text=f"{get_month(month)} {year}",
                                       callback_data=f"dummy"))
    markup.row()

    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    for weekday in weekdays:
        markup.insert(InlineKeyboardButton(text=weekday, callback_data="dummy"))

    num_days = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]
    last_weekday = calendar.weekday(year, month, num_days)

    for day in range(1, num_days + 1):

        current_day = datetime.date(year, month, day)
        day_of_week = current_day.weekday()

        if day == 1:
            [markup.insert(InlineKeyboardButton(text=" ", callback_data="dummy")) for _ in range(first_weekday)]

        check_day = day if int(day)>9 else f'0{day}'
        check_month = month if int(month)>9 else f'0{month}'
        check_date = f'{year}-{check_month}-{check_day}'

        if len(db.check_date(check_date, worker)) == 2 and check_date >= str(datetime.datetime.today())[:10]:
            button_text = str(day)
            button_callback = f"day_{day}_{month}_{year}"
            markup.insert(InlineKeyboardButton(text=button_text, callback_data=button_callback))
        else:
            markup.insert(InlineKeyboardButton(text=' ', callback_data='dummy'))

    [markup.insert(InlineKeyboardButton(text=" ", callback_data="dummy")) for _ in range(6-last_weekday)]

    next_month = datetime.datetime(year, month, num_days) + datetime.timedelta(days=1)
    markup.row()
    markup.insert(InlineKeyboardButton(text="<<", callback_data=f"prev_{previous_month.month}_{previous_month.year}"))
    markup.insert(InlineKeyboardButton(text=">>", callback_data=f"next_{next_month.month}_{next_month.year}"))

    return markup

async def show_calendar(message, year, month, worker):
    markup = generate_calendar(year, month, worker)
    await message.answer(f'Выберите день для записи на сеанс:', reply_markup=markup)


def generate_calendar_for_day_off(year, month, worker):
    markup = InlineKeyboardMarkup(row_width=7)

    previous_month = datetime.datetime(year, month, 1) - datetime.timedelta(days=1)
    markup.insert(InlineKeyboardButton(text=f"{get_month(month)} {year}",
                                       callback_data=f"dummy"))
    markup.row()

    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    for weekday in weekdays:
        markup.insert(InlineKeyboardButton(text=weekday, callback_data="dummy"))

    num_days = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]
    last_weekday = calendar.weekday(year, month, num_days)

    for day in range(1, num_days + 1):

        current_day = datetime.date(year, month, day)
        day_of_week = current_day.weekday()

        if day == 1:
            [markup.insert(InlineKeyboardButton(text=" ", callback_data="dummy")) for _ in range(first_weekday)]

        check_day = day if int(day)>9 else f'0{day}'
        check_month = month if int(month)>9 else f'0{month}'
        check_date = f'{year}-{check_month}-{check_day}'

        if len(db.check_date(check_date, worker)) == 2 and check_date >= str(datetime.datetime.today())[:10]:
            button_text = str(day)
            button_callback = f"off_{day}_{month}_{year}"
            markup.insert(InlineKeyboardButton(text=button_text, callback_data=button_callback))
        else:
            markup.insert(InlineKeyboardButton(text=' ', callback_data='dummy'))

    [markup.insert(InlineKeyboardButton(text=" ", callback_data="dummy")) for _ in range(6-last_weekday)]

    next_month = datetime.datetime(year, month, num_days) + datetime.timedelta(days=1)
    markup.row()
    markup.insert(InlineKeyboardButton(text="<<", callback_data=f"prev_{previous_month.month}_{previous_month.year}"))
    markup.insert(InlineKeyboardButton(text=">>", callback_data=f"next_{next_month.month}_{next_month.year}"))

    return markup

async def show_calendar_for_day_off(message, year, month, worker):
    markup = generate_calendar_for_day_off(year, month, worker)
    await message.answer(f'Выберите день выходного:', reply_markup=markup)