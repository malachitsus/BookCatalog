from dataclasses import asdict
import json
from .book import Book
from .catalog import BookCatalog
from .constants import JSON_FORMAT_VERSION, JSON_ENCODING, JSON_INDENT, JSON_ENSURE_ASCII
from .exceptions import (
    CorruptedFileError,
    DuplicateIdError,
    InvalidBookError,
    UnsupportedFormatVersionError,
)

def save_catalog(catalog: BookCatalog, path: str) -> None:
    """Сохраняет все поля книг и версию формата в JSON-файл."""
    books = []
    for book in catalog:
        books.append(asdict(book))

    data = {
        "format_version": JSON_FORMAT_VERSION,
        "books": books,
    }

    with open(path, "w", encoding=JSON_ENCODING) as file:
        json.dump(data, file, ensure_ascii=JSON_ENSURE_ASCII, indent=JSON_INDENT)

def load_catalog(catalog: BookCatalog, path: str) -> None:
    """Заменяет каталог данными JSON только после полной проверки файла."""
    try:
        with open(path, "r", encoding=JSON_ENCODING) as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise CorruptedFileError("Invalid JSON") from error

    if not isinstance(data, dict):
        raise CorruptedFileError("Document must be an object")

    if "format_version" not in data or "books" not in data:
        raise CorruptedFileError("Missing required fields")

    if not isinstance(data["books"], list):
        raise CorruptedFileError("Field 'books' must be a list")

    if type(data["format_version"]) is not int or data["format_version"] != JSON_FORMAT_VERSION:
        raise UnsupportedFormatVersionError("Unsupported format version")

    temp = BookCatalog()
    for book_data in data["books"]:
        if not isinstance(book_data, dict):
            raise CorruptedFileError("Each book must be an object")
        try:
            book = Book(**book_data)
            temp.add_book(book)
        except (TypeError, InvalidBookError, DuplicateIdError) as error:
            raise CorruptedFileError("Invalid book data") from error

    catalog._items = temp._items
