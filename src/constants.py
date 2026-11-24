"""Константы форматов хранения и импорта каталога."""


JSON_FORMAT_VERSION: int = 1
JSON_ENCODING: str = "utf-8"
JSON_INDENT: int = 4
JSON_ENSURE_ASCII: bool = False

CSV_ENCODING: str = "utf-8-sig"
CSV_DELIMITER: str = ","
CSV_FIELDS: tuple[str, ...] = ("id", "name", "category", "author", "year", "pages")

DEFAULT_CATALOG_PATH: str = "books.json"
CLI_ERROR_EXIT_CODE: int = 1
