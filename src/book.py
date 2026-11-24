from dataclasses import dataclass
from .exceptions import InvalidBookError


@dataclass(frozen=True)
class Book:
    id: str
    name: str
    category: str
    author: str
    year: int
    pages: int

    def __post_init__(self) -> None:
        """Проверяет поля книги; при неверных значениях вызывает InvalidBookError."""
        for value in (self.id, self.name, self.category, self.author):
            if not isinstance(value, str) or not value.strip():
                raise InvalidBookError("Text fields must be non-empty strings")
        if type(self.year) is not int or self.year <= 0:
            raise InvalidBookError("Field 'year' must be positive integer")
        if type(self.pages) is not int or self.pages <= 0:
            raise InvalidBookError("Field 'pages' must be positive integer")
