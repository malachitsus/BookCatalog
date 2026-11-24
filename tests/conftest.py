import pytest
from src.book import Book
from src.catalog import BookCatalog


@pytest.fixture
def book() -> Book:
    """Создаёт корректную книгу для тестов."""
    return Book("1", "Война и мир", "Роман", "Лев Толстой", 1869, 1225)


@pytest.fixture
def catalog(book: Book) -> BookCatalog:
    """Создаёт каталог с одной книгой."""
    result = BookCatalog()
    result.add_book(book)
    return result
