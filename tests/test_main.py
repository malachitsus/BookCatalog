"""Проверки командной строки каталога."""

import json
import sys
from pathlib import Path

import pytest

from src.main import main


def run_command(monkeypatch: pytest.MonkeyPatch, path: Path, *arguments: str) -> None:
    """Вызывает main с аргументами команды и временным файлом каталога."""
    monkeypatch.setattr(sys, "argv", ["bookcatalog", "--file", str(path), *arguments])
    main()


def test_add_find_remove(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Команды добавляют, находят и удаляют книгу между запусками."""
    path = tmp_path / "books.json"
    run_command(monkeypatch, path, "add", "--id", "1", "--name", "War and Peace",
                "--author", "Tolstoy", "--category", "Novel", "--year", "1869", "--pages", "1225")
    assert json.loads(path.read_text(encoding="utf-8"))["books"][0]["id"] == "1"
    for arguments in [("list",), ("get", "1"), ("find", "--name", "WAR"), ("find", "--category", "Novel")]:
        capsys.readouterr()
        run_command(monkeypatch, path, *arguments)
        assert "War and Peace" in capsys.readouterr().out
    run_command(monkeypatch, path, "remove", "1")
    assert json.loads(path.read_text(encoding="utf-8"))["books"] == []


def test_csv_import(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Команда импорта записывает CSV-книги в JSON."""
    source = tmp_path / "books.csv"
    source.write_text("id,name,category,author,year,pages\n1,Book,Novel,Author,2000,100\n", encoding="utf-8")
    path = tmp_path / "books.json"
    run_command(monkeypatch, path, "import", str(source))
    assert json.loads(path.read_text(encoding="utf-8"))["books"][0]["name"] == "Book"
    before = path.read_bytes()
    with pytest.raises(SystemExit) as error:
        run_command(monkeypatch, path, "import", str(source))
    assert error.value.code == 1
    assert path.read_bytes() == before


def test_bad_json_unchanged(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Повреждённый каталог не перезаписывается и ошибка выводится без traceback."""
    path = tmp_path / "books.json"
    path.write_text("broken", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        run_command(monkeypatch, path, "remove", "1")
    assert error.value.code == 1
    assert path.read_text(encoding="utf-8") == "broken"
    assert "Ошибка:" in capsys.readouterr().err


def test_empty_catalog(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Просмотр нового каталога не создаёт файл."""
    path = tmp_path / "books.json"
    run_command(monkeypatch, path, "list")
    assert "Книг нет" in capsys.readouterr().out
    assert not path.exists()
    with pytest.raises(SystemExit):
        run_command(monkeypatch, path, "get", "missing")
    assert not path.exists()


def test_invalid_arguments(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Парсер отклоняет неполную команду и несовместимые условия поиска."""
    path = tmp_path / "books.json"
    for args in [("add",), ("find", "--name", "Book", "--category", "Novel")]:
        with pytest.raises(SystemExit) as error:
            run_command(monkeypatch, path, *args)
        assert error.value.code == 2
    assert not path.exists()
