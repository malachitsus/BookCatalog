from .book import Book
from .exceptions import DuplicateIdError, BookNotFoundError
from collections.abc import Iterator

class BookCatalog:
    def __init__(self) -> None:
        """Создаёт пустой каталог книг."""
        self._items: dict[str, Book] = {}

    def add_book(self, item: Book) -> None:
        """Добавляет книгу; при занятом ID вызывает DuplicateIdError."""
        if item.id in self._items:
            raise DuplicateIdError("A book with this ID already exists")
        self._items[item.id] = item

    def get_book(self, item_id: str) -> Book:
        """Возвращает книгу по ID; если её нет, вызывает BookNotFoundError."""
        if item_id not in self._items:
            raise BookNotFoundError("Book not found!")
        return self._items[item_id]

    def remove_book(self, item_id: str) -> None:
        """Удаляет книгу по ID; если её нет, вызывает BookNotFoundError."""
        if item_id not in self._items:
            raise BookNotFoundError("Book not found!")
        del self._items[item_id]

    def find_by_category(self, category: str) -> list[Book]:
        """Возвращает новый список книг указанной категории в порядке добавления."""
        found = []
        for book in self._items.values():
            if book.category == category:
                found.append(book)
        return found

    def find_by_name(self, query: str) -> list[Book]:
        """Возвращает новый список книг с фрагментом названия без учёта регистра."""
        found = []
        query = query.casefold()
        for book in self._items.values():
            if query in book.name.casefold():
                found.append(book)
        return found

    def __len__(self) -> int:
        """Возвращает количество книг в каталоге."""
        return len(self._items)

    def __contains__(self, item_id: str) -> bool:
        """Проверяет наличие книги с указанным ID."""
        return item_id in self._items

    def __iter__(self) -> Iterator[Book]:
        """Возвращает итератор по книгам в порядке их добавления."""
        return iter(self._items.values())
