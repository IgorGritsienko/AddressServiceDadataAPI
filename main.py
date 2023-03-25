# -*- coding: utf-8 -*-
import db
import json
import requests

clear = "\n" * 100
db_path = './users.db'
resource = 'address'

BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'


API_KEY = ''


def get_current_option(param):
    conn = db.create_connection(db_path)
    curr_option = db.select_user_info(conn, param)
    return conn, curr_option


def restore_url(conn, param, base_url):
    db.update_user(conn, param, base_url)


def edit_url(param):
    conn, curr_url = get_current_option(param)
    curr_url = curr_url[0]
    print(f'\nТекущий URL: {curr_url}')
    print('Введите новый URL:')
    print('\'0\' для возврата в меню, \'00\' для сброса к базовому URL.')
    new_url = input()
    match new_url:
        case '0':
            pass
        case '00':
            restore_url(conn, param, BASE_URL)
        case _:
            db.update_user(conn, param, new_url)
    conn.close()
    return


def edit_api(param):

    conn, curr_api = get_current_option(param)
    curr_api = curr_api[0]
    print(f'\nТекущий API: {curr_api}')
    new_api = input('Введите новый API или \'0\' для возвращения в меню:')
    match new_api:
        case 0:
            pass
        case _:
            db.update_user(conn, param, new_api)
    conn.close()
    return


def edit_lang(param):

    conn, curr_lang = get_current_option(param)

    if curr_lang[0] == 'ru':
        new_lang = 'en'
    else:
        new_lang = 'ru'

    print(f'\nТекущий язык: {curr_lang[0]}')
    print(f'Изменить на {new_lang}?')
    print('1. Да.\n0. Назад.')
    ans = input()

    match ans:
        case '1':
            db.update_user(conn, param, new_lang)
    conn.close()
    return


def get_search_query():
    query = input('\nВведите строку для поиска в соответствии с правилами сервиса нахождения адресов Dadata:')
    return query


def get_user_info():
    conn, user_info = get_current_option('_')
    conn.close()
    return user_info

def search(resource, query, base_url, api_key, lang):
    url = base_url + resource
    headers = {
        'Authorization': 'Token ' + api_key,
        'Content-Type': 'application/json',
        'Accept':'application/json'
    }
    data = {
        'query': query,
        'language': lang
    }
    try:
        res = requests.post(url, data=json.dumps(data), headers=headers)
    except requests.exceptions.RequestException as err:
        print(f'Ошибка!\n{err}')
        return 0
    return res.json()


def print_search_results(res):
    if len(res['suggestions']) == 0:
        print ('\nНичего не найдено...')
    else:
        print('\nМесто: ', res['suggestions'][0]['value'])
        print('Координаты широты: ', res['suggestions'][0]['data']['geo_lat'])
        print('Координаты долготы: ', res['suggestions'][0]['data']['geo_lon'])


def options():
    while True:
        print('\nДоступные опции:\n')
        print('1. Редактировать URL.')
        print('2. Редактировать API ключ.')
        print('3. Выбрать язык результата запроса.\n Русский - "ru" \n Английский - "en"')
        print('0. Назад.')

        user_choice = input('\nВыберите действие: ')
        match user_choice:
            case '1':
                edit_url(user_choice)
            case '2':
                edit_api(user_choice)
            case '3':
                edit_lang(user_choice)
            case '0':
                break
            case _:
                print(clear)


def menu():
    db.check_db_existence(db_path)
    while True:
        print('\nФункционал программы:\n')
        print('1. Получить координаты адреса.')
        print('2. Опции пользователя.')
        print('0. Выход из программы.')

        user_choice = input('\nВыберите действие: ')
        match user_choice:
            case '1':
                query = get_search_query()
                user_info = get_user_info()
                res = search(resource, query, user_info[1], API_KEY, user_info[3])
                if res:
                    print_search_results(res)
            case '2':
                options()
            case '0':
                break
            case _:
                print(clear)
    print('\nПрограмма завершила свою работу.\n')

def main():
    menu()


if __name__ == "__main__":
    main()
