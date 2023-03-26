import os.path
import sqlite3
from sqlite3 import Error


create_users_table = """
CREATE TABLE IF NOT EXISTS users(
    user_id INT PRIMARY KEY,
    default_URL TEXT DEFAULT 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/',
    API_key TEXT,
    language TEXT DEFAULT 'ru' CHECK (language IN ('ru', 'en'))
);
"""

insert_user_table = """
INSERT INTO users(user_id, API_key)
            VALUES(?, ?);
"""


class Options:
    DEFAULT_URL = '1'
    API_KEY = '2'
    LANGUAGE = '3'


def check_db_existence(db_path):
    if not os.path.isfile(db_path):
        conn = create_connection(db_path)
        create_table(conn, create_users_table)
        insert_user(conn, insert_user_table)
        conn.close()


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
    except Error as e:
        print(f'Произошла ошибка: {e}')
    return conn


def create_table(conn, query):
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
    except Error as e:
        print(f'Произошла ошибка: {e}')


# создание заглушки в виде единственного пользователя с unique id = 1
def insert_user(conn, query):
    cur = conn.cursor()
    default_user = ('1', '')
    try:
        cur.execute(query, default_user)
        conn.commit()
    except Error as e:
        print(f'Произошла ошибка: {e}')



def select_user_info(conn, param):
    # вместо авторизации, хардкод идентификатора пользователя, всегда один и тот же
    default_user = 1

    match param:
        case Options.DEFAULT_URL:
            column_name = 'default_URL'
        case Options.API_KEY:
            column_name = 'API_key'
        case Options.LANGUAGE:
            column_name = 'language'
        case _:
            column_name = '*'

    select_query = f"SELECT {column_name} FROM users WHERE user_id = {default_user};"
    cur = conn.cursor()

    try:
        cur.execute(select_query)
        res = cur.fetchone()
        return res
    except Error as e:
        print(f"Произошла ошибка: {e}")


def update_user(conn, param, value):
    # вместо авторизации, хардкод идентификатора пользователя, всегда один и тот же
    default_user = 1

    match param:
        case Options.DEFAULT_URL:
            column_name = 'default_URL'
        case Options.API_KEY:
            column_name = 'API_key'
        case Options.LANGUAGE:
            column_name = 'language'

    update_query = f"UPDATE users SET {column_name} = '{value}' WHERE user_id = {default_user};"
    cur = conn.cursor()

    try:
        cur.execute(update_query)
        conn.commit()
    except Error as e:
        print(f"Произошла ошибка: {e}")
