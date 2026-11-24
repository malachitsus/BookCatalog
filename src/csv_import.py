"""Добавление книг из CSV-файла."""

import csv

from .book import Book
from .catalog import BookCatalog
from .constants import CSV_ENCODING, CSV_DELIMITER, CSV_FIELDS
from .exceptions import CorruptedFileError, DuplicateIdError, InvalidBookError


def import_csv(catalog: BookCatalog, path: str) -> int:
    """Проверяет CSV и добавляет книги; при ошибке каталог не меняется."""
    temporary = BookCatalog()
    line = 1
    try:
        with open(path, encoding=CSV_ENCODING, newline="") as file:
            reader = csv.DictReader(file, delimiter=CSV_DELIMITER, strict=True)
            if sorted(reader.fieldnames or []) != sorted(CSV_FIELDS):
                raise CorruptedFileError("Invalid CSV columns")

            for row in reader:
                line = reader.line_num
                if None in row or None in row.values():
                    raise CorruptedFileError(f"CSV line {line}: wrong number of fields")
                book = Book(
                    id=row["id"], name=row["name"], category=row["category"],
                    author=row["author"], year=int(row["year"]), pages=int(row["pages"]),
                )
                if book.id in catalog:
                    raise DuplicateIdError("This ID already exists in the catalog")
                temporary.add_book(book)
    except (ValueError, TypeError, csv.Error, InvalidBookError, DuplicateIdError) as error:
        raise CorruptedFileError(f"CSV line {line}: {error}") from error

    for book in temporary:
        catalog.add_book(book)
    return len(temporary)
