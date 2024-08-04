import datetime
import sqlite3 as sq

db = sq.connect('Database/tattoes.db')
cur = db.cursor()

def db_start():

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER     PRIMARY KEY, 
    username            TEXT, 
    name                TEXT,
    number              TEXT)''')
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS sessions (
    id     INTEGER  PRIMARY KEY AUTOINCREMENT,
    worker TEXT,
    client TEXT,
    date   DATETIME,
    time   TEXT);''')
    db.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS workers (
    user_id     INTEGER PRIMARY KEY
                        REFERENCES users (user_id) ON DELETE CASCADE,
    username    TEXT,
    name        TEXT,
    photos      TEXT,
    description TEXT,
    admin       BOOL);''')  #
    db.commit()


    cur.execute('PRAGMA foreign_keys = ON')
    db.commit()


def create_profile(user_id, username):
    user = cur.execute(f"SELECT 1 FROM users WHERE user_id == '{user_id}'").fetchone()

    if not user:
        cur.execute(f'INSERT INTO users(user_id, username) VALUES("{user_id}", "{username}")')
        db.commit()


def check_user_info(user_id):
    number = cur.execute(f'SELECT number FROM users WHERE "user_id"=="{user_id}"').fetchone()
    if number[0] == None:
        return 0
    else:
        return 1


def check_admin(user_id):
    return cur.execute(f'SELECT 1 FROM workers WHERE "user_id"=="{user_id}" AND "admin"=="1"').fetchone()


def add_user_info(user_id, name, number):
    cur.execute(f'UPDATE users SET "name"="{name}", "number"="{number}" WHERE "user_id" == "{user_id}"')
    db.commit()


def check_worker(user_id):
    worker = cur.execute(f"SELECT 1 FROM workers WHERE user_id == '{user_id}'").fetchone()

    if not worker:
        return 0
    else:
        return 1


def get_incoming_sessions(worker_id):
    today = str(datetime.datetime.now().date())
    sessions = cur.execute(f'SELECT id, client, date, time, username FROM sessions JOIN workers ON sessions.worker=workers.username WHERE "date" >= "{today}" and "worker" = "{worker_id}"').fetchall()

    if sessions:
        formated_sessions = f'Список записей к @{sessions[0][4]}\n\n'
        for session in sessions:
            id = session[0]
            client_id = session[1]
            date = session[2]
            time = session[3]

            client_info = cur.execute(f'SELECT username, name, number FROM users WHERE "user_id" == "{client_id}"').fetchone()
            if client_info:
                client_username, client_name, client_number = client_info[0], client_info[1], client_info[2]
                formated_sessions += f'{id}. @{client_username} {client_name} ({client_number}) {date} {time}\n'
        
        return formated_sessions
    else:
        
        return 'У Вас нет записей на ближайшее время'


def get_workers():
    return cur.execute('SELECT * FROM workers').fetchall()

def check_session(client_id):
    return cur.execute(f'SELECT 1 FROM sessions WHERE "client" == "{client_id}" AND "date" >= {str(datetime.datetime.today())[:10]}').fetchone()


def get_client_sessions(client_id):
    return cur.execute(f'SELECT id, worker, date, time FROM sessions WHERE "client" == "{client_id}"').fetchall()


def cancel_session(session_id):
    try:
        cur.execute(f'DELETE FROM sessions WHERE "id"=="{session_id}"')
        db.commit()
        
        return 'Запись удалена!'
    
    except:
        
        return 'Запись не найдена!'


def check_date(date, worker):
    sessions = cur.execute(f'SELECT * FROM sessions WHERE "worker" == "{worker}" AND "date" == "{date}"').fetchall()

    allowed_time = ['9:00', '14:00']

    for session in sessions:
        allowed_time.remove(session[4])

    return allowed_time


def create_session(worker_username, client_id, date, time):
    if check_date(date, worker_username):
        cur.execute(f'INSERT INTO sessions(worker, client, date, time) VALUES("{worker_username}", "{client_id}", "{date}", "{time}")')
        db.commit()
        
        return f'Вы успешно записались к @{worker_username} на {date} {time}!'
    
    else:
        
        return f'К сожалению, это время уже занято!'


def day_off(worker_username, date):
    cur.execute(f'INSERT INTO sessions(worker, client, date, time) VALUES ("{worker_username}", "Выходной","{date}", "9:00")')
    db.commit()


def add_worker(user_id, username, name, photos, description):
    cur.execute(f'INSERT INTO workers(user_id, username, name, photos, description) '
                f'VALUES("{user_id}", "{username}", "{name}", "{photos}", "{description}")')
    db.commit()


def remove_worker(user_id):
    cur.execute(f'DELETE FROM workers WHERE "user_id" == "{user_id}"')
    db.commit()


def find_worker(username):
    return cur.execute(f'SELECT user_id FROM users WHERE "username" == "{username}"').fetchone()[0]



if __name__ == '__main__':
    db_start()
