# BookCatalog

Лабораторная работа № 3. Каталог библиотечных книг на Python 3.12 и новее.
Можно добавлять, искать и удалять книги, сохранять каталог в JSON и загружать книги из CSV.

Установка из папки проекта:

```bash
python -m pip install -e .
```

Общая справка и справка по отдельной команде:

```bash
bookcatalog --help
bookcatalog add --help
bookcatalog import --help
```

Примеры команд:

```bash
bookcatalog import books.csv
bookcatalog find --name "дуб"
bookcatalog find --category "Роман"
bookcatalog add --id 1 --name "Дубровский" --category "Роман" --author "Пушкин" --year 1841 --pages 224
bookcatalog list
bookcatalog get 1
bookcatalog remove 1

```

Данные хранятся в books.json в текущей папке. Другой файл указывается перед командой: `bookcatalog --file library.json list`.

Для CSV нужна кодировка UTF-8 и такие колонки:

```csv
id,name,category,author,year,pages
2,Война и мир,Роман,Толстой,1869,1225
```

ID не должны повторяться. Текстовые поля не могут быть пустыми, год и число страниц должны быть положительными целыми числами.
Поиск названия работает по фрагменту без учёта регистра, поиск категории — по точному совпадению.
Книги перебираются в порядке добавления. При удалении и повторном добавлении книга перемещается в конец.

JSON содержит поля format_version (версия 1) и books (список книг). Загрузка заменяет каталог, импорт CSV дополняет его.
При ошибке проверки файла каталог не изменяется.

В папке src: book.py — книга, catalog.py — каталог, storage.py — JSON, csv_import.py — CSV,
main.py — команды, exceptions.py — ошибки, constants.py — константы.

Тесты находятся в tests. Запуск:

```bash
python -m pytest
```

Удаление пакета (в том же окружении Python, где он установлен):

```bash
python -m pip uninstall bookcatalog
```

Исходники проекта и файлы с книгами при этом не удаляются, их можно удалить только вручную.
