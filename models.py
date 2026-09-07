from datetime import datetime, timezone
from math import isfinite
from uuid import uuid4


class BaseItem:
    item_type = "base"

    def __init__(self, id=None, created_at=None):
        self.id = str(uuid4()) if id is None else id

        self.created_at = (
            datetime.now(timezone.utc)
            if created_at is None
            else created_at
        )

    def to_dict(self):
        return {
            "type": self.item_type,
            "id": self.id,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    def __str__(self):
        return f"{self.item_type}: {self.id}"


class Note(BaseItem):
    item_type = "note"

    def __init__(self, text, id=None, created_at=None):
        super().__init__(id=id, created_at=created_at)

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Текст заметки не должен быть пустым")

        self.text = text.strip()

    def to_dict(self):
        data = super().to_dict()
        data["text"] = self.text
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data["text"],
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    def __str__(self):
        return self.text


class Reminder(BaseItem):
    item_type = "reminder"

    def __init__(self, text, remind_at, id=None, created_at=None):
        super().__init__(id=id, created_at=created_at)

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Текст напоминания не должен быть пустым")

        if not isinstance(remind_at, datetime):
            raise TypeError("remind_at должен быть объектом datetime")

        self.text = text.strip()
        self.remind_at = remind_at

    def to_dict(self):
        data = super().to_dict()
        data["text"] = self.text
        data["remind_at"] = self.remind_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data["text"],
            remind_at=datetime.fromisoformat(data["remind_at"]),
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    def __str__(self):
        return f"{self.text} — {self.remind_at:%d.%m.%Y %H:%M}"


class Expense(BaseItem):
    item_type = "expense"

    def __init__(self, amount, category, id=None, created_at=None):
        super().__init__(id=id, created_at=created_at)

        self.amount = amount

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Категория не должна быть пустой")

        self.category = category.strip()

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        value = float(value)

        if not isfinite(value) or value <= 0:
            raise ValueError(
                "Сумма должна быть положительным конечным числом"
            )

        self._amount = value

    def to_dict(self):
        data = super().to_dict()
        data["amount"] = self.amount
        data["category"] = self.category
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            amount=data["amount"],
            category=data["category"],
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    def __str__(self):
        return f"{self.amount:.2f} ₽ — {self.category}"