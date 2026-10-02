import pytest
from app.models.book import Book


def test_from_dict():
    # Arrange
    book_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    book = Book.from_dict(book_data)

    # Assert
    assert book.title == "New Book"
    assert book.description == "The Best!"


def test_from_dict_missing_title():
    # Arrange
    book_data = {
        "description": "The Best!"
    }

    # Act & Assert
    with pytest.raises(KeyError):
        Book.from_dict(book_data)


def test_from_dict_missing_description():
    # Arrange
    book_data = {
        "title": "New Book"
    }

    # Act & Assert
    with pytest.raises(KeyError):
        Book.from_dict(book_data)


def test_from_dict_with_extra_key():
    # Arrange
    book_data = {
        "title": "New Book",
        "description": "The Best!",
        "extra": "Extra Data"
    }

    # Act
    book = Book.from_dict(book_data)

    # Assert
    assert book.title == "New Book"
    assert book.description == "The Best!"