from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from werkzeug.exceptions import HTTPException
from app.models.book import Book
from app.models.author import Author
import pytest


def test_validate_model_with_valid_id(app):
    # Arrange
    book = Book(
        title="Test Book",
        description="Test Description"
    )

    with app.app_context():
        from app.db import db
        db.session.add(book)
        db.session.commit()

        # Act
        result = validate_model(Book, book.id)

        # Assert
        assert result.id == book.id
        assert result.title == "Test Book"
        assert result.description == "Test Description"


def test_validate_model_with_invalid_id(app):
    # Act & Assert
    with app.app_context():
        with pytest.raises(HTTPException) as error:
            validate_model(Book, 1)

        response = error.value.response
        assert response.status_code == 404


def test_create_model_book(client):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    result = create_model(Book, test_data)

    # Assert
    assert isinstance(result, tuple)
    assert result[0]["id"] == 1
    assert result[0]["title"] == "New Book"
    assert result[0]["description"] == "The Best!"
    assert result[1] == 201


def test_create_model_book_missing_data(client):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act & Assert
    # Calling `create_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached
    with pytest.raises(HTTPException) as error:
        create_model(Book, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"


def test_create_model_author(client):
    # Arrange
    test_data = {
        "name": "New Author"
    }

    # Act
    result = create_model(Author, test_data)

    # Assert
    assert isinstance(result, tuple)
    assert result[0]["id"] == 1
    assert result[0]["name"] == "New Author"
    assert result[1] == 201


def test_get_models_with_filters_one_matching_book(two_saved_books):
    # Act
    result = get_models_with_filters(Book, {"title": "ocean"})

    # Assert
    assert result == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }]