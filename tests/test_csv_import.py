"""Основные проверки импорта CSV."""

from pathlib import Path

import pytest

from src.catalog import BookCatalog
from src.csv_import import import_csv
from src.exceptions import CorruptedFileError


def test_import_csv(tmp_path: Path) -> None:
    """Корректная строка становится книгой в каталоге."""
    path = tmp_path / "books.csv"
    path.write_text(
        'id,name,category,author,year,pages\n'
        '1,"Книга, том первый",Роман,Автор,2020,100\n',
        encoding="utf-8",
    )
    catalog = BookCatalog()
    assert import_csv(catalog, str(path)) == 1
    book = catalog.get_book("1")
    assert book.name == "Книга, том первый"
    assert book.author == "Автор"
    assert book.category == "Роман"
    assert book.year == 2020
    assert book.pages == 100


def test_invalid_rows(tmp_path: Path) -> None:
    """Отбрасывает явный мусор без частичного добавления книг."""
    bad_rows = [
        "3,Name,Category,Author,wrong,100",  # Год не число.
        "3,Name,Category,Author,2020,0",     # Ноль страниц.
        "3, ,Category,Author,2020,100",      # Пустое название.
        "3,Name,Category,Author,2020",       # Не хватает поля.
        "3,Name,Category,Author,2020,100,extra",  # Лишнее поле.
        "2,Other,Category,Author,2020,100",   # Дубликат внутри CSV.
        '3,"Unclosed',                       # Незакрытые кавычки.
    ]
    path = tmp_path / "bad.csv"
    for row in bad_rows:
        catalog = BookCatalog()
        path.write_text(
            "id,name,category,author,year,pages\n"
            "2,Valid,Category,Author,2020,100\n" + row + "\n",
            encoding="utf-8",
        )
        with pytest.raises(CorruptedFileError):
            import_csv(catalog, str(path))
        assert len(catalog) == 0


def test_existing_id(catalog: BookCatalog, tmp_path: Path) -> None:
    """Дубликат существующего ID не меняет каталог."""
    before = list(catalog)
    path = tmp_path / "duplicate.csv"
    path.write_text(
        "id,name,category,author,year,pages\n"
        "2,New,Category,Author,2020,100\n"
        "1,Duplicate,Category,Author,2020,100\n",
        encoding="utf-8",
    )
    with pytest.raises(CorruptedFileError):
        import_csv(catalog, str(path))
    assert list(catalog) == before


def test_invalid_header(tmp_path: Path) -> None:
    """Отбрасывает пустой файл и неверный заголовок."""
    path = tmp_path / "header.csv"
    for text in ["", "garbage", "id,name\n1,Book"]:
        path.write_text(text, encoding="utf-8")
        with pytest.raises(CorruptedFileError):
            import_csv(BookCatalog(), str(path))


def test_header_only(tmp_path: Path) -> None:
    """Заголовок без записей добавляет ноль книг."""
    path = tmp_path / "empty.csv"
    path.write_text("id,name,category,author,year,pages\n", encoding="utf-8")
    catalog = BookCatalog()
    assert import_csv(catalog, str(path)) == 0
    assert len(catalog) == 0
