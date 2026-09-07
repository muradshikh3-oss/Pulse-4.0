import json
from datetime import datetime, timezone

import pytest

from models import BaseItem, Expense, Note, Reminder
from storage import Storage


def test_missing_file_is_empty(tmp_path):
    storage = Storage(tmp_path / "data.json")

    assert storage.get_all(BaseItem) == []


def test_add_and_get_all(tmp_path):
    storage = Storage(tmp_path / "data.json")

    note = Note("Молоко")
    expense = Expense(100, "еда")

    storage.add(note)
    storage.add(expense)

    assert storage.get_all(Note) == [note]
    assert storage.get_all(Expense) == [expense]
    assert storage.get_all(Reminder) == []


def test_delete_is_persistent(tmp_path):
    path = tmp_path / "data.json"
    storage = Storage(path)

    first = Note("Удалить")
    second = Note("Оставить")

    storage.add(first)
    storage.add(second)

    assert storage.delete(first.id) is True
    assert storage.delete("unknown-id") is False

    restored = Storage(path).get_all(Note)

    assert len(restored) == 1
    assert restored[0].id == second.id


def test_persistence_keeps_types_ids_dates_and_values(tmp_path):
    path = tmp_path / "data.json"
    storage = Storage(path)

    items = [
        Note("Купить молоко"),
        Expense(250.75, "еда"),
        Reminder(
            "Встреча",
            datetime(
                2026, 9, 8, 15,
                tzinfo=timezone.utc,
            ),
        ),
    ]

    for item in items:
        storage.add(item)

    restored = Storage(path).get_all(BaseItem)

    assert [type(item) for item in restored] == [
        Note,
        Expense,
        Reminder,
    ]

    assert [vars(item) for item in restored] == [
        vars(item) for item in items
    ]


def test_explicit_save_and_load(tmp_path):
    path = tmp_path / "data.json"

    first = Storage(path)
    note = Note("До изменения")

    first.add(note)

    second = Storage(path)

    note.text = "После изменения"
    first.save()

    second.load()

    assert second.get_all(Note)[0].text == "После изменения"


def test_legacy_json_is_preserved_and_converted(tmp_path):
    path = tmp_path / "data.json"

    old_data = {
        "notes": ["Старая заметка"],
        "expenses": [
            {
                "amount": 150,
                "category": "еда",
            }
        ],
    }

    path.write_text(
        json.dumps(old_data, ensure_ascii=False),
        encoding="utf-8",
    )

    original = path.read_bytes()

    storage = Storage(path)

    assert storage.get_all(Note)[0].text == "Старая заметка"
    assert storage.get_all(Expense)[0].amount == 150

    # Сама загрузка не должна переписывать файл.
    assert path.read_bytes() == original

    storage.add(Note("Новая заметка"))

    restored = Storage(path)

    assert [
        note.text
        for note in restored.get_all(Note)
    ] == [
        "Старая заметка",
        "Новая заметка",
    ]

    assert restored.get_all(Expense)[0].category == "еда"


def test_broken_json_is_not_overwritten(tmp_path):
    path = tmp_path / "data.json"

    path.write_text(
        "{broken json",
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        Storage(path)

    assert path.read_text(
        encoding="utf-8"
    ) == "{broken json"


def test_duplicate_id_is_rejected(tmp_path):
    storage = Storage(tmp_path / "data.json")

    storage.add(
        Note("Первая", id="same")
    )

    with pytest.raises(ValueError):
        storage.add(
            Note("Вторая", id="same")
        )

    assert len(storage.get_all(Note)) == 1