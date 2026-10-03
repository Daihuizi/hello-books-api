


# “”“现在你有三个 endpoint：
# POST /books          → 创建一本
# GET  /books          → 读取所有 books
# GET  /books/<book_id> → 读取指定的一本

# 并且 validate_book() 负责：
# book_id 不是数字 → 400
# book 不存在      → 404
# book 存在        → return Book object”“”

from flask import Blueprint, request
from app.models.book import Book
from .route_utilities import create_model, validate_model, get_models_with_filters
from ..db import db


bp = Blueprint("books_bp", __name__, url_prefix="/books")


@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)


@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)


@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return book.to_dict()


@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return {"details": f'Book {book.id} "{book.title}" successfully deleted'}