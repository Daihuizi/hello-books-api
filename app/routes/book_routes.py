


# “”“现在你有三个 endpoint：
# POST /books          → 创建一本
# GET  /books          → 读取所有 books
# GET  /books/<book_id> → 读取指定的一本

# 并且 validate_book() 负责：
# book_id 不是数字 → 400
# book 不存在      → 404
# book 存在        → return Book object”“”

from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db


books_bp = Blueprint("books_bp", __name__, url_prefix="/books")


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({"message": f"book {book_id} invalid"}, 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))

    return book


@books_bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)
    except KeyError:
        return {"message": "Invalid data"}, 400

    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }

    return response, 201


@books_bp.get("")
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    query = query.order_by(Book.id)
    books = db.session.scalars(query)

    books_response = []

    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description,
            }
        )

    return books_response


@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }


@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")