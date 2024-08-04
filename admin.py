import Database.database as db

from openpyxl import Workbook

async def get_all_records(bot, id):
	sessions = db.cur.execute('SELECT * FROM sessions').fetchall()

	wb = Workbook()
	sessions_file = wb.active

	for row in sessions:
		sessions_file.append(row)

	users = db.cur.execute('SELECT * FROM users').fetchall()
	users_file = wb.create_sheet('users')

	for row in users:
		users_file.append(row)

	wb.save('records.xlsx')
	with open('records.xlsx', 'rb') as file:
		await bot.send_document(id, file)



