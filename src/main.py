"""Управление каталогом из командной строки."""

import argparse
import sys

from .book import Book
from .catalog import BookCatalog
from .constants import DEFAULT_CATALOG_PATH, CLI_ERROR_EXIT_CODE
from .csv_import import import_csv
from .exceptions import CatalogError
from .storage import load_catalog, save_catalog


def create_parser() -> argparse.ArgumentParser:
    """Описывает команды и аргументы программы."""
    parser = argparse.ArgumentParser(prog="bookcatalog", description="Каталог книг")
    parser.add_argument("--file", default=DEFAULT_CATALOG_PATH, help="Путь к JSON-каталогу")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="Показать все книги")

    add = commands.add_parser("add", help="Добавить книгу")
    add.add_argument("--id", required=True, help="Уникальный ID")
    add.add_argument("--name", required=True, help="Название")
    add.add_argument("--category", required=True, help="Категория")
    add.add_argument("--author", required=True, help="Автор")
    add.add_argument("--year", required=True, type=int, help="Год издания")
    add.add_argument("--pages", required=True, type=int, help="Количество страниц")

    get = commands.add_parser("get", help="Получить книгу по ID")
    get.add_argument("id", help="ID книги")

    remove = commands.add_parser("remove", help="Удалить книгу по ID")
    remove.add_argument("id", help="ID книги")

    find = commands.add_parser("find", help="Найти книги")
    search = find.add_mutually_exclusive_group(required=True)
    search.add_argument("--name", help="Фрагмент названия без учёта регистра")
    search.add_argument("--category", help="Точная категория")

    csv_import = commands.add_parser("import", help="Добавить книги из CSV")
    csv_import.add_argument("path", help="Путь к CSV-файлу")
    return parser


def print_books(books: list[Book]) -> None:
    """Выводит поля книг или сообщение об отсутствии результатов."""
    if not books:
        print("Книг нет.")
    for book in books:
        print(f"{book.id} | {book.name} | {book.author} | "
              f"{book.category} | {book.year} | {book.pages} стр.")


def main() -> None:
    """Загружает каталог, выполняет команду и сохраняет изменения."""
    args = create_parser().parse_args()
    catalog = BookCatalog()

    try:
        try:
            load_catalog(catalog, args.file)
        except FileNotFoundError:
            pass  # При первом запуске каталог ещё не сохранён.

        if args.command == "list":
            print_books(list(catalog))
        elif args.command == "get":
            print_books([catalog.get_book(args.id)])
        elif args.command == "find":
            if args.name is not None:
                books = catalog.find_by_name(args.name)
            else:
                books = catalog.find_by_category(args.category)
            print_books(books)
        elif args.command == "add":
            book = Book(args.id, args.name, args.category, args.author, args.year, args.pages)
            catalog.add_book(book)
            save_catalog(catalog, args.file)
            print(f"Книга {book.id} добавлена.")
        elif args.command == "remove":
            catalog.remove_book(args.id)
            save_catalog(catalog, args.file)
            print(f"Книга {args.id} удалена.")
        elif args.command == "import":
            count = import_csv(catalog, args.path)
            save_catalog(catalog, args.file)
            print(f"Добавлено книг: {count}.")
    except (CatalogError, OSError, UnicodeError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        raise SystemExit(CLI_ERROR_EXIT_CODE) from error


if __name__ == "__main__":
    main()
