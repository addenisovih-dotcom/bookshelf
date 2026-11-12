from flask_login import UserMixin

from lib.extensions import db

# можливі статуси книги
STATUSES = {
    "want": "Хочу прочитати",
    "reading": "Читаю",
    "done": "Прочитано",
}


# модель користувача
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    books = db.relationship("Book", backref="owner", lazy=True)


# модель книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="want")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @property
    def status_label(self):
        return STATUSES.get(self.status, self.status)
