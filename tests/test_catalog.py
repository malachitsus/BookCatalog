"""Проверки операций каталога."""

import pytest
from src.book import Book
from src.catalog import BookCatalog
from src.exceptions import BookNotFoundError, DuplicateIdError


def test_add_get_remove(book: Book) -> None:
    """Книга добавляется, получается по ID и удаляется."""
    catalog = BookCatalog()
    assert len(catalog) == 0
    assert list(catalog) == []
    catalog.add_book(book)
    assert catalog.get_book(book.id) is book
    assert book.id in catalog
    assert len(catalog) == 1
    catalog.remove_book(book.id)
    assert book.id not in catalog
    assert len(catalog) == 0
    assert catalog.find_by_category(book.category) == []
    assert catalog.find_by_name(book.name) == []


def test_duplicate(catalog: BookCatalog, book: Book) -> None:
    """Повторный ID не перезаписывает исходную книгу."""
    other = Book(book.id, "Other", "Other", "Author", 2000, 10)
    with pytest.raises(DuplicateIdError):
        catalog.add_book(other)
    assert list(catalog) == [book]


def test_missing_get(catalog: BookCatalog, book: Book) -> None:
    """Получение отсутствующей книги вызывает предметную ошибку."""
    with pytest.raises(BookNotFoundError):
        catalog.get_book("missing")
    assert list(catalog) == [book]


def test_missing_remove(catalog: BookCatalog, book: Book) -> None:
    """Удаление отсутствующей книги вызывает предметную ошибку."""
    with pytest.raises(BookNotFoundError):
        catalog.remove_book("missing")
    assert list(catalog) == [book]


def test_search(catalog: BookCatalog, book: Book) -> None:
    """Поиск проверяет категорию и фрагмент названия без учёта регистра."""
    other = Book("2", "Мир животных", "Наука", "Автор", 2000, 100)
    catalog.add_book(other)
    assert catalog.find_by_category("Роман") == [book]
    assert catalog.find_by_name("МИР") == [book, other]
    assert catalog.find_by_name("missing") == []
    assert catalog.find_by_category("missing") == []


def test_search_lists(catalog: BookCatalog, book: Book) -> None:
    """Очистка результатов поиска не удаляет книги из каталога."""
    by_name = catalog.find_by_name("война")
    by_category = catalog.find_by_category("Роман")
    by_name.clear()
    by_category.clear()
    assert list(catalog) == [book]
    assert catalog.find_by_name("война") == [book]
    assert catalog.find_by_category("Роман") == [book]


def test_iteration(catalog: BookCatalog, book: Book) -> None:
    """Повторный обход сохраняет порядок добавления."""
    other = Book("2", "Other", "Novel", "Author", 2000, 100)
    catalog.add_book(other)
    assert list(catalog) == [book, other]
    assert list(catalog) == [book, other]
    catalog.remove_book(book.id)
    catalog.add_book(book)
    assert list(catalog) == [other, book]
