import time

from flask import Flask
from sqlalchemy.exc import OperationalError

from lib.config import Config
from lib.extensions import db, login_manager
from lib.models import User
from routes.auth import auth_bp
from routes.books import books_bp


def init_db(app):
    # чекаємо, поки MySQL буде готовий приймати з'єднання
    with app.app_context():
        for _ in range(30):
            try:
                db.create_all()
                return
            except OperationalError:
                time.sleep(2)
        db.create_all()


def create_app():
    # 1
    app = Flask(__name__)
    app.config.from_object(Config)
    # 2
    db.init_app(app)
    login_manager.init_app(app)

    # 3
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # 4
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)

    # 5
    init_db(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
