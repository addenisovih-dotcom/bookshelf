from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from lib.extensions import db
from lib.models import STATUSES, Book

books_bp = Blueprint("books", __name__)


def get_own_book(book_id):
    # книга має належати поточному користувачу
    return Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()


@books_bp.route("/")
@login_required
def index():
    books = Book.query.filter_by(user_id=current_user.id).order_by(Book.title).all()
    return render_template("books/list.html", books=books)


@books_bp.route("/books/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("books/form.html", book=None, statuses=STATUSES)

    title = (request.form.get("title") or "").strip()
    author = (request.form.get("author") or "").strip()
    status = request.form.get("status", "want")
    if not title or not author or status not in STATUSES:
        flash("Заповніть назву та автора!")
        return redirect(url_for("books.add"))

    db.session.add(Book(title=title, author=author, status=status, user_id=current_user.id))
    db.session.commit()
    flash("Книгу додано.")
    return redirect(url_for("books.index"))


@books_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit(book_id):
    book = get_own_book(book_id)
    if request.method == "GET":
        return render_template("books/form.html", book=book, statuses=STATUSES)

    title = (request.form.get("title") or "").strip()
    author = (request.form.get("author") or "").strip()
    status = request.form.get("status", book.status)
    if not title or not author or status not in STATUSES:
        flash("Заповніть назву та автора!")
        return redirect(url_for("books.edit", book_id=book.id))

    book.title = title
    book.author = author
    book.status = status
    db.session.commit()
    flash("Зміни збережено.")
    return redirect(url_for("books.index"))


@books_bp.route("/books/<int:book_id>/delete", methods=["POST"])
@login_required
def delete(book_id):
    book = get_own_book(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Книгу видалено.")
    return redirect(url_for("books.index"))
