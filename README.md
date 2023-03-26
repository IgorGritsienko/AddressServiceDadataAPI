# AddressServiceDadataAPI
Getting address coordinates via Dadata API

# Документация ПО AddressServiceDadataAPI


При запуске программы появится меню, предлагающее следующие варианты действий:

1. Основной функционал программы - получить координаты адреса.

Данная функция использует настройки пользователя:

    - URL, к которому происходит обращение (по умолчанию - https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/).

    - API ключ (по умолчанию отсутствует, находится по ссылке https://dadata.ru/profile/#info после регистрации и авторизации на сайте) сервиса dadata.

    - Язык результата запроса (по умолчанию - русский).

При выборе данного варианта требуется указать строку запроса, на основании которой будет произведено вычисление географической широты и долготы. В качестве строки запроса может служить страна, город, улица, дом и т.д.

При возникновении какой-либо ошибки будет выведено соответствующее сообщение.
При отсутствии результатов поиска на запрос будет выведено сообщение об отсутствии результатов.

При успешном выполнении пользователю будет предоставлен список результатов по запросу. Пользователь выбирает один из предложенных ему вариантов указанием соответствующего результату числа,
после чего получает географическую широту и долготу по выбранному им адресу.

2. Опции пользователя.

Позволяют изменить перечисленные в пункте 1 настройки пользователя.
При выборе данного варианта появится меню, которое содержит в себе изменение URL, API и языка.
При выборе любого из предложенных вариантов будет показано текущее значение опции с возможностью изменить ее.

    - Меню редактирования URL позволяет изменить URL, вернуть базовый URL или вернуться в предыдущее меню.
    
    - Меню редактирования API позволяет изменить API или вернуться в предыдущее меню.
    
    - Меню изменения языка позволяет сделать выбор между русский и английским языком.

3. Выход из программы.

Завершение работы программы с текстовым оповещением.
