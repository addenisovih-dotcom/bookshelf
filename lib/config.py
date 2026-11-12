import os
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # параметри підключення до MySQL
    DB_USER = os.environ.get("MYSQL_USER", "root")
    DB_PASS = os.environ.get("MYSQL_PASSWORD", "root")
    DB_HOST = os.environ.get("MYSQL_HOST", "localhost")
    DB_NAME = os.environ.get("MYSQL_DATABASE", "bookshelf_db")

    # DATABASE_URL дозволяє підставити іншу БД (наприклад, sqlite для тестів)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
