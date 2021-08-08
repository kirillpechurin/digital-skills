# Сервис по отслеживанию статистики ребенка

### Для работы
`pip install -r requirements.txt`

### Дальше создать файл `load_env.py`. В нем прописать:

- Для работы с БД
  - `PG_HOST`
  - `PG_PORT`
  - `USER`
  - `PASSWORD`
  - `DB_NAME`
- Для работы с отправкой писем на Email
  - `MAIL_HOST`
  - `MAIL_PORT`
  - `MAIL_FROM`
  - `MAIL_PASSWORD`
- Настройки flask
  - `HOST`
  - `PORT`
  - `DEBUG`
- Дополнительные настройки
  - `SECRET_KEY_SESSION`
  - `SECRET_KEY`
  - `ENCRYPT_ALGORITHM`
  - `LIFETIME_CODE`
  - `SEND_CODE_INTERVAL`
