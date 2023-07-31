# Сервис рассылок
Данный сайт - сервис рассылок, где пользователь может сформировать свою базу клиентов, которым с заданной периодичностью (Раз в день, Раз в неделю, Раз в месяц) будет отправляться на электронную почту сформированное письмо.

## Установка и запуск
1. Создать базу данных Postgres для проекта.
2. Создать и настроить `.env` файл в корне проекта по образцу `.env.sample`
3. Из корня проекта в терминале выполнить:
    - Установить зависимости проекта: `poetry install`
    - Активировать виртуальное окружение: `poetry shell`
    - Применить миграции: `python manage.py migrate`
    - Создать суперпользователя: `python manage.py csu`
     По умолчанию логин: `1`, пароль: `1`
    - Создать группы с правами: `python manage.py create_groups`
    - Запустить сервер: `python manage.py runserver`

## Группы и права

По-умолчанию в работе сайта предусмотрено три группы:

- `standard-user`
**Может через интерфейс сайта:**
- - Создавать, удалять, редактировать, просматривать своих клиентов.
- - Создавать, удалять, редактировать, просматривать свои рассылки.
- - Создавать, удалять, редактировать, просматривать свои настройки рассылки.
- - Просматривать свои логи рассылки.
- - Просматривать статьи из блога
---
- `manager`
**Может через интерфейс сайта:**
- - Просматривать Активировать и деактивировать, всех пользователей сервиса.
- - Просматривать Активировать и деактивировать, все рассылки сервиса.
- - Просматривать статьи из блога
---
- `content-manager`
**Может через админ-панель:**
- - Создавать, удалять, редактировать, просматривать статьи из блога.
---
>При регистрации пользователю автоматически присваивается 
группа `standard-user`

>Распределение пользователей по группам `manager` и `content-manager` 
производит администратор через админ панель.

## Как это работает

При создании рассылки, на основе введенных данных и email-адресов клиентов, которых добавил пользователь формируется crontab задача и записывается в систему linux.

При редактировании crontab задачи она удаляется и записывается заново с обновленными данными.

Если при создании crontab задачи указано время окончания рассылки, то по достижении этого времени задача автоматически удалится из системы, а статус рассылки поменяется на "Отключена"

Если время начала рассылки меньше текущего времени, рассылка начнется сразу после ее создания.

>Так же из директории можно осуществить **разовую** рассылку выполнив команду и передав аргументы:
```
- Coursework_6
    | - services - 
    |   | - cron_jobs
```


`./send_emails.py "Тема сообщения" "Текст сообщения" "Список email адресов через пробел"`

## Структура проекта
```
- Coursework_6 - корень проекта
    | - blog 
    |
    | - client_management
    |
    | - mailing_management - главное приложение
    |   | - templates
    |   |   | - mailing_management
    |   |   |   | - index.html - Главная страница сайта
    |
    | - config - настройки проекта
    |
    | - services - утилиты для проекта
    |   | - cron_jobs
    |   |   | - send_emails.py - скрипт выполняемый crontab`ом при рассылке
    |
    | - static
    |
    | - users
    |   | - management
    |   |   | - commands
    |   |   |   | - create_groups.py - Команда создания групп с правами
    |   |   |   | - csu.py - Команда создания суперпользователя
```
