import json
from datetime import datetime, timezone

import pytest

from models import BaseItem, Expense, Note, Reminder


def test_creation():
    before = datetime.now(timezone.utc)

    note = Note("Купить молоко")

    assert isinstance(note, BaseItem)
    assert note.text == "Купить молоко"
    assert note.id != Note("Другая заметка").id

    assert (
        before
        <= note.created_at
        <= datetime.now(timezone.utc)
    )


def test_note_to_dict():
    created = datetime(
        2026, 9, 7, 12,
        tzinfo=timezone.utc,
    )

    note = Note(
        "Учить Python",
        id="note-1",
        created_at=created,
    )

    assert note.to_dict() == {
        "type": "note",
        "id": "note-1",
        "created_at": "2026-09-07T12:00:00+00:00",
        "text": "Учить Python",
    }


def test_note_from_dict():
    note = Note.from_dict({
        "type": "note",
        "id": "saved-id",
        "created_at": "2026-09-01T10:30:00+00:00",
        "text": "Старая заметка",
    })

    assert note.id == "saved-id"
    assert note.text == "Старая заметка"

    assert note.created_at == datetime(
        2026, 9, 1, 10, 30,
        tzinfo=timezone.utc,
    )


@pytest.mark.parametrize(
    "item",
    [
        BaseItem(),
        Note("Купить молоко"),
        Reminder(
            "Встреча",
            datetime(
                2026, 9, 8, 15,
                tzinfo=timezone.utc,
            ),
        ),
        Expense(150.50, "еда"),
    ],
)
def test_json_round_trip(item):
    data = json.loads(
        json.dumps(item.to_dict())
    )

    restored = type(item).from_dict(data)

    assert type(restored) is type(item)
    assert restored is not item
    assert vars(restored) == vars(item)


def test_str():
    assert str(Note("Учить Python")) == "Учить Python"

    assert str(Expense(150, "еда")) == "150.00 ₽ — еда"

    reminder = Reminder(
        "Встреча",
        datetime(2026, 9, 8, 15),
    )

    assert str(reminder) == "Встреча — 08.09.2026 15:00"


@pytest.mark.parametrize(
    "amount",
    [0, -1, float("nan"), float("inf")],
)
def test_expense_rejects_invalid_amount(amount):
    with pytest.raises(ValueError):
        Expense(amount, "еда")


def test_property_checks_later_assignment():
    expense = Expense(100, "еда")

    expense.amount = 250

    assert expense.amount == 250

    with pytest.raises(ValueError):
        expense.amount = -50

    assert expense.amount == 250