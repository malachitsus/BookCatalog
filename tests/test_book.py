"""Проверки данных книги."""

from dataclasses import FrozenInstanceError
import pytest
from src.book import Book
from src.exceptions import InvalidBookError


def test_valid_book() -> None:
    """Книга сохраняет переданные поля."""
    book = Book("1", "Дубровский", "Роман", "Пушкин", 1841, 224)
    assert book.id == "1"
    assert book.name == "Дубровский"
    assert book.category == "Роман"
    assert book.author == "Пушкин"
    assert book.year == 1841
    assert book.pages == 224


def test_invalid_fields() -> None:
    """Пустые строки, неверные типы и неположительные числа запрещены."""
    data = dict(id="1", name="Book", category="Novel", author="Author", year=2000, pages=100)
    for field in ("id", "name", "category", "author"):
        for value in ("", "   ", None, 42):
            bad = dict(data)
            bad[field] = value
            with pytest.raises(InvalidBookError):
                Book(**bad)
    for field in ("year", "pages"):
        for value in (0, -1, 1.5, "10", None, True, False):
            bad = dict(data)
            bad[field] = value
            with pytest.raises(InvalidBookError):
                Book(**bad)


def test_book_cannot_change(book: Book) -> None:
    """После проверки нельзя испортить поля книги, в том числе её ID."""
    with pytest.raises(FrozenInstanceError):
        book.id = "other"  # type: ignore[misc]
