import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot import BotController
from models import Expense, Note
from storage import Storage


def make_update():
    message = SimpleNamespace(
        reply_text=AsyncMock()
    )

    return SimpleNamespace(
        effective_message=message
    )


def test_note_and_notes_after_restart(tmp_path):
    path = tmp_path / "data.json"

    controller = BotController(Storage(path))
    update = make_update()

    asyncio.run(
        controller.handle_note(
            update,
            SimpleNamespace(
                args=["Купить", "молоко"]
            ),
        )
    )

    update.effective_message.reply_text.assert_awaited_once_with(
        "Заметка добавлена: Купить молоко"
    )

    restarted = BotController(Storage(path))
    update = make_update()

    asyncio.run(
        restarted.handle_notes(
            update,
            SimpleNamespace(args=[]),
        )
    )

    update.effective_message.reply_text.assert_awaited_once_with(
        "1. Купить молоко"
    )


def test_empty_note_is_not_saved(tmp_path):
    storage = Storage(tmp_path / "data.json")
    update = make_update()

    asyncio.run(
        BotController(storage).handle_note(
            update,
            SimpleNamespace(args=[]),
        )
    )

    assert storage.get_all(Note) == []

    update.effective_message.reply_text.assert_awaited_once_with(
        "Использование: /note текст"
    )


def test_expenses_add_and_list(tmp_path):
    storage = Storage(tmp_path / "data.json")
    controller = BotController(storage)

    update = make_update()

    asyncio.run(
        controller.handle_expenses(
            update,
            SimpleNamespace(
                args=["150,50", "еда"]
            ),
        )
    )

    asyncio.run(
        controller.handle_expenses(
            update,
            SimpleNamespace(
                args=["50", "проезд"]
            ),
        )
    )

    assert len(storage.get_all(Expense)) == 2

    update = make_update()

    asyncio.run(
        controller.handle_expenses(
            update,
            SimpleNamespace(args=[]),
        )
    )

    update.effective_message.reply_text.assert_awaited_once_with(
        "1. 150.50 ₽ — еда\n"
        "2. 50.00 ₽ — проезд\n"
        "Итого: 200.50 ₽"
    )


@pytest.mark.parametrize(
    "args",
    [
        ["abc", "еда"],
        ["-10", "еда"],
        ["150"],
    ],
)
def test_invalid_expense_is_not_saved(tmp_path, args):
    storage = Storage(tmp_path / "data.json")
    update = make_update()

    asyncio.run(
        BotController(storage).handle_expenses(
            update,
            SimpleNamespace(args=args),
        )
    )

    assert storage.get_all(Expense) == []

    update.effective_message.reply_text.assert_awaited_once()


@pytest.mark.parametrize(
    "method,expected",
    [
        ("handle_notes", "Заметок пока нет."),
        ("handle_expenses", "Расходов пока нет."),
    ],
)
def test_empty_lists(tmp_path, method, expected):
    controller = BotController(
        Storage(tmp_path / "data.json")
    )

    update = make_update()

    asyncio.run(
        getattr(controller, method)(
            update,
            SimpleNamespace(args=[]),
        )
    )

    update.effective_message.reply_text.assert_awaited_once_with(
        expected
    )