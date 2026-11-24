import json
from dataclasses import asdict
from pathlib import Path
import pytest
from src.book import Book
from src.catalog import BookCatalog
from src.storage import load_catalog, save_catalog
from src.exceptions import CorruptedFileError, UnsupportedFormatVersionError


def test_round_trip(catalog: BookCatalog, book: Book, tmp_path: Path) -> None:
    """Проверяет сохранение всех полей и замену каталога при загрузке JSON."""
    second = Book("2", "Second", "Other", "Author", 2020, 30)
    catalog.add_book(second)
    path = tmp_path / "books.json"
    save_catalog(catalog, str(path))
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "format_version": 1, "books": [asdict(book), asdict(second)]}
    target = BookCatalog()
    target.add_book(Book("old", "Old", "Other", "Author", 2000, 1))
    load_catalog(target, str(path))
    assert list(target) == [book, second]
    assert "old" not in target


def test_empty_round_trip(catalog: BookCatalog, tmp_path: Path) -> None:
    """Проверяет загрузку пустого каталога вместо существующих книг."""
    path = tmp_path / "empty.json"
    save_catalog(BookCatalog(), str(path))
    load_catalog(catalog, str(path))
    assert list(catalog) == []


def test_bad_documents(catalog: BookCatalog, book: Book, tmp_path: Path) -> None:
    """Неверный JSON и структура не меняют существующий каталог."""
    path = tmp_path / "bad.json"
    documents = ["{", "", "[]", "null", "{}", '{"format_version":1}',
                 '{"books":[]}', '{"format_version":1,"books":{}}',
                 '{"format_version":1,"books":[null]}']
    for document in documents:
        path.write_text(document, encoding="utf-8")
        with pytest.raises(CorruptedFileError):
            load_catalog(catalog, str(path))
        assert list(catalog) == [book]


def test_bad_versions(catalog: BookCatalog, book: Book, tmp_path: Path) -> None:
    """Неизвестная версия отклоняется без изменения каталога."""
    path = tmp_path / "version.json"
    for version in (2, "1", None, True, 1.0):
        path.write_text(json.dumps({"format_version": version, "books": []}), encoding="utf-8")
        with pytest.raises(UnsupportedFormatVersionError):
            load_catalog(catalog, str(path))
        assert list(catalog) == [book]


def test_atomic_load(catalog: BookCatalog, book: Book, tmp_path: Path) -> None:
    """Ошибка второй книги не позволяет добавить первую."""
    first = asdict(Book("new", "New", "Novel", "Author", 2000, 100))
    bad_books = [dict(first, id="other", pages=-1),
                 {"id": "missing-fields"}, dict(first, extra="value"), first]
    path = tmp_path / "partial.json"
    for bad in bad_books:
        data = {"format_version": 1, "books": [first, bad]}
        path.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(CorruptedFileError):
            load_catalog(catalog, str(path))
        assert list(catalog) == [book]
        assert catalog.get_book(book.id) is book
        assert "new" not in catalog
