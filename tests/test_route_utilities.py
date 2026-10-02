from app.routes.route_utilities import validate_model
from app.models.book import Book


def test_validate_model_with_valid_id(app, two_saved_books):
    # Act
    with app.app_context():
        book = validate_model(Book, 1)

        # Assert
        assert book.id == 1
        assert book.title == "Ocean Book"
        assert book.description == "watr 4evr"


def test_validate_model_with_invalid_id(app):
    # Act & Assert
    with app.app_context():
        try:
            validate_model(Book, 1)
        except Exception as error:
            assert error.response.status_code == 404


def test_validate_model_with_invalid_id_format(app):
    # Act & Assert
    with app.app_context():
        try:
            validate_model(Book, "abc")
        except Exception as error:
            assert error.response.status_code == 400

def test_update_one_book(client, two_saved_books):
    # Act
    response = client.put("/books/1", json={
        "title": "Updated Book",
        "description": "Updated Description"
    })

    # Assert
    assert response.status_code == 204

def test_delete_one_book(client, two_saved_books):
    # Act
    response = client.delete("/books/1")

    # Assert
    assert response.status_code == 204