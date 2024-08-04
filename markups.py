from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

to_menu = InlineKeyboardButton('🏠 Главное меню', callback_data='main_menu')
to_menu_only = InlineKeyboardMarkup(row_width=1).add(to_menu)

# -- Главное меню --

to_workers = InlineKeyboardButton('🚹 Выбрать мастера', callback_data='to_workers')
client_sessions = InlineKeyboardButton('📝 Показать записи', callback_data='client_show_sessions')
address= InlineKeyboardButton('🗺️ Адрес', callback_data='show_adresses')
about_us = InlineKeyboardButton('ℹ️ О нас', callback_data='about_us')
main_menu = InlineKeyboardMarkup(row_width=1).add(to_workers, client_sessions,address, about_us)


# -- Меню работника --

worker_sessions = InlineKeyboardButton('Показать записи', callback_data='show_sessions')
worker_day_off = InlineKeyboardButton('Взять выходной', callback_data='weekend')
worker_menu = InlineKeyboardMarkup(row_width=1).add(worker_sessions, worker_day_off)

# -- Админ меню --

admin_get_all_sessions = InlineKeyboardButton('Получить все записи', callback_data='get_all_records')
admin_add_worker = InlineKeyboardButton('Добавить работника', callback_data='add_worker')
admin_delete_worker = InlineKeyboardButton('Удалить работника', callback_data='delete_worker')
admin_menu = InlineKeyboardMarkup(row_width=1).add(admin_get_all_sessions, admin_add_worker, admin_delete_worker)


session_apply_button = InlineKeyboardButton('✍ Записаться', callback_data='apply_session')
session_apply_markup = InlineKeyboardMarkup(row_width=1).add(session_apply_button, to_menu)