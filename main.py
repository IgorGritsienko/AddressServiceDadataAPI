# -*- coding: utf-8 -*-
import db
import json
import requests

clear = "\n" * 100
db_path = './users6.db'
resource = 'address'

BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'


API_KEY = ''


def get_current_option(param):
    # Подключение к БД и извлечение данных о текущем пользователе
    
    conn = db.create_connection(db_path)
    curr_option = db.select_user_info(conn, param)
    return conn, curr_option


def restore_url(conn, param, base_url):
    # Возврат к базовому URL
    
    db.update_user(conn, param, base_url)


def edit_url(param):
    # Функция, получающая текущий URL пользователя
    # и при необходимости изменяющая его
    
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
    # Функция, получающая текущий API пользователя
    # и при необходимости изменяющая его
    
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
    # Функция, получающая текущий язык результата запроса пользователя
    # и при необходимости изменяющая его
    
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
    # Получение всех параметров пользователя
    
    conn, user_info = get_current_option('_')
    conn.close()
    return user_info


def get_search_params():
    # Получение строки запроса и параметров пользователя
    
    query = get_search_query()
    user_info = get_user_info()
    
    data = {
        'query': query,
        'language': user_info[3]
    }
    
    return query, user_info, data


def search(resource, query, base_url, api_key, data):
    # Создание URL, заголовков и отправка запроса
    
    url = base_url + resource
    headers = {
        'Authorization': 'Token ' + api_key,
        'Content-Type': 'application/json',
        'Accept':'application/json'
    }
    try:
        res = requests.post(url, data=json.dumps(data), headers=headers)
    except requests.exceptions.RequestException as err:
        print(f'Ошибка!\n{err}')
        return 0
    
    return res.json()


def get_search_results(res):
    
    if len(res['suggestions']) == 0:
        print ('\nНичего не найдено...')
        return 0
    else:
        # Создание списка, получающегося при распаковке
        # (результат - порядковый номер)
        
        res_list = []
        
        for i, j in zip(res['suggestions'], range(10)):
            row = i['value']
            print(f'{j+1}: {row}')
            res_list.append(row)
        return res_list

def print_search_results(res):
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
                query, user_info, data = get_search_params()
                result = search(resource, query, user_info[1], API_KEY, data)
                
                # проверка на рабочий URL
                if result:
                    res_list = get_search_results(result)
                    
                    # проверка на нахождение данных по запросу
                    if res_list:
                        while True:
                            user_final_choice = input(f'Выберите вариант из предложенных (от 1 до {len(res_list)}): ')
                            try:
                                # перевод строки в число
                                user_final_choice_num = int(user_final_choice)
                                # если число удовлетворяет условиям, то выходим из цикла
                                if (user_final_choice_num >= 1 and user_final_choice_num <= len(res_list)):
                                    break
                                else:
                                    print(f'Введите число от 1 до {len(res_list)}!')
                            except:
                                print('Введите число!')
                        # изменяем данные в словаре на конкретную выбранную строкк запроса
                        # количество выводимых записей = 1
                        data['query'] = res_list[user_final_choice_num - 1]
                        data['count'] = 1
                        single_result = search(resource, query, user_info[1], API_KEY, data)
                        print_search_results(single_result)

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
