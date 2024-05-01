# Digital Skills | Сервис по отслеживанию успеваемости

___

1. [Цель проекта](#цель-проекта)
2. [Реализация](#реализация)
    + [Техническая реализация](#техническая-реализация)
    + [Бизнес-задачи](#бизнес-задачи)
3. [Структура проекта](#структура-проекта)
4. [Описание переменных окружения](#описание-переменных-окружения)
5. [Запуск](#запуск)
    + [Зависимости](#зависимости)
    + [Запуск локального сервера](#запуск-локального-сервера)

___

## Цель проекта

Сервис направлен на отслеживание успеваемости ребенка в различных мероприятиях и
образовательных учреждениях.

Благодаря сервису:

- Организация, проводившая мероприятие, может занести результаты для каждого участвовавшего.
- Родитель может видеть активность своих детей на пройденных мероприятиях.

## Реализация

___

### Техническая реализация

* Веб-приложение реализовано с использованием [Flask](https://flask.palletsprojects.com/en/2.3.x/).
* В качестве основной СУБД используется PostgreSQL.
* Для взаимодействия с БД используется ORM [SQLAlchemy](https://www.sqlalchemy.org/).
* Для авторизации и аутентификации используется JWT.
* Отправка писем с помощью SMTP (gmail).

### Бизнес-задачи

* Реализовано два типа регистрации - для родителя и организации.
* Пользователи в своем личном кабинете могут изменить пароль.
* Родители могут добавить ребенка для отслеживания статистики по нему.
* Организация может создать, изменить, удалить событие.
* Организация может указать достижения для каждого события.
* Родитель может отправить заявку на регистрацию ребенка на событие.
* Организация может принять или отклонить заявку.
* Организация может назначить достижения за проведенное событие ребенку.
* Родитель может на отдельной странице увидеть всю успеваемость ребенка.

## Структура проекта

___

- `docs` - Документация проекта.
- `portfolio` - Веб-приложение.
    - `bootstrap` - Подгрузка данных, при запуске приложения.
    - `configs` - Конфигурация веб-приложения.
    - `drivers` - Драйверы (серверы), использующиеся в веб-приложении.
    - `enums` - Перечисления (в т.ч. ошибки).
    - `internal`
        - `biz` - Бизнес-логика веб-приложения.
            - `dao` - Слой DAO.
            - `deserializers` - Десериализация данных.
            - `serializers` - Сериализация данных.
            - `services` - Услуги, предоставляемые бизнес-логикой.
            - `validators` - Валидация данных.
        - `http` - API веб-приложения.
    - `models` - Модели веб-приложения.
    - `templates` - Шаблоны веб-приложения.
    - `.env.example` - Пример файла переменных окружения.
    - `main.py` - Скрипт для старта веб-приложения.
    - `requirements.txt` - Зависимости.
    - `setup.py` - Скрипт для подготовки веб-приложения.

## Описание переменных окружения

___

* `HTTP_HOST` - Хост, на котором будет запущено веб-приложение.
* `HTTP_PORT` - Порт, на котором будет запущено веб-приложение.
* `DEBUG` - Режим отладки (0 или 1).
* `DB_HOST` - Хост, на котором запущена БД.
* `DB_PORT` - Порт, на котором запущена БД.
* `DB_USER` - Пользователь БД.
* `DB_PASSWORD` - Пароль для пользователя БД.
* `DB_NAME` - Наименование БД.
* `MAIL_HOST` - Хост SMTP сервера.
* `MAIL_PORT` - Порт SMTP сервера.
* `MAIL_FROM` - Адрес электронной почты - пользователь SMTP сервера.
* `MAIL_PASSWORD` - Пароль для пользователя SMTP сервера.
* `SECRET_KEY_SESSION` - Секретный ключ сессии.
* `SECRET_KEY` - Секретный ключ веб-приложения.
* `ENCRYPT_ALGORITHM` - Алгоритм шифрования (JWT).
* `LIFETIME_CODE` - Время жизни кода для подтверждения учётной записи.
* `SEND_CODE_INTERVAL` - Время, необходимое для возможности переотправки кода
  для подтверждения учётной записи.

## Запуск

___

### Зависимости

* Установленный python `3.8`.
* Убедитесь, что установлены и запущены следующие сервисы:
    * `postgresql`

### Запуск локального сервера

1. Создайте PostgreSQL БД, которая будет использоваться в проекте.
2. Создайте файл `portfolio/.env` и укажите переменные окружения аналогично примеру `portfolio/.env.example`.
3. `python3 -m venv venv` - Создайте виртуальное окружение.
4. `source venv/bin/activate` - Активируйте виртуальное окружение.
5. `pip3 install -r requirements.txt` - Установите зависимости.
6. `python setup.py` - Запустите скрипт подготовки проекта.
7. Вы готовы к запуску!
   Для запуска локального сервера запустите ниже приведенную команду:
   ```shell
   python main.py
   ```
   Если вы указали `HTTP_HOST=0.0.0.0`, `HTTP_PORT=8000`,
   ваш локальный сервер будет доступен по ссылке [http://0.0.0.0:8000](http://0.0.0.0:8000)
