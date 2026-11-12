# BookShelf

Прототип вебзастосунку «Особиста бібліотека» на Flask + MySQL. Побудований за принципами навчального проєкту ContactsApp: Blueprint-и, Flask-SQLAlchemy, Flask-Login, хешування паролів, окремі користувачі зі своїми записами.

## Функціональність

- реєстрація, вхід і вихід користувача (`routes/auth.py`);
- додавання, редагування і видалення книг (`routes/books.py`);
- кожен користувач бачить і змінює лише свої книги;
- книга має статус: «Хочу прочитати», «Читаю», «Прочитано».

## Структура

```
bookshelf/
├── app.py
├── lib/
│   ├── config.py
│   ├── extensions.py
│   └── models.py
├── routes/
│   ├── auth.py
│   └── books.py
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── books/
│       ├── list.html
│       └── form.html
├── static/style.css
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Запуск через Docker Compose

```
docker compose up --build
```

Сайт: http://localhost:8080. Таблиці створюються автоматично при старті.

## Запуск локально

Потрібен запущений MySQL і база `bookshelf_db`.

```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS
pip install -r requirements.txt
python app.py
```

Сайт: http://127.0.0.1:5000

Параметри підключення задаються змінними середовища (значення за замовчуванням у дужках): `MYSQL_USER` (root), `MYSQL_PASSWORD` (root), `MYSQL_HOST` (localhost), `MYSQL_DATABASE` (bookshelf_db), `SECRET_KEY`.
