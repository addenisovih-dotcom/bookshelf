from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from lib.extensions import db
from lib.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # логіка реєстрації
    if current_user.is_authenticated:
        return redirect(url_for("books.index"))

    if request.method == "GET":
        return render_template("auth/register.html", is_required=True)

    # 1
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        flash("Заповніть ім'я користувача та пароль!")
        return redirect(url_for("auth.register"))
    # 2 перевірка користувача з таким іменем
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Користувач з таким іменем вже існує!")
        return redirect(url_for("auth.register"))
    # 3 хешування пароля
    hashed_password = generate_password_hash(password, method="scrypt")
    new_user = User(username=username, password=hashed_password)
    # 4 зберігання і коміт
    db.session.add(new_user)
    db.session.commit()
    # 5 сформувати повідомлення
    flash("Реєстрацію успішно завершено! Увійдіть у систему.")
    return redirect(url_for("auth.login"))


# вхід користувача
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("books.index"))

    if request.method == "GET":
        return render_template("auth/login.html", is_required=True)

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    remember = bool(request.form.get("remember"))
    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        flash("Невірне ім'я користувача або пароль!")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    # переходимо на попередню сторінку, лише якщо це внутрішній шлях
    next_url = request.args.get("next", "")
    if next_url and not urlparse(next_url).netloc and next_url.startswith("/"):
        return redirect(next_url)
    return redirect(url_for("books.index"))


# вихід користувача
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.")
    return redirect(url_for("auth.login"))
