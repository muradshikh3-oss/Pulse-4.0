import json
from pathlib import Path

from models import BaseItem, Expense, Note, Reminder


class Storage:
    MODEL_TYPES = {
        "base": BaseItem,
        "note": Note,
        "reminder": Reminder,
        "expense": Expense,
    }

    def __init__(self, filename="data.json"):
        self._path = Path(filename)
        self._items = []
        self.load()

    def save(self):
        data = [item.to_dict() for item in self._items]

        self._path.parent.mkdir(parents=True, exist_ok=True)

        # Сначала записываем во временный файл.
        temp_path = self._path.with_suffix(
            self._path.suffix + ".tmp"
        )

        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )

        temp_path.replace(self._path)

    def load(self):
        try:
            with self._path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            self._items = []
            return []

        if isinstance(data, dict):
            if set(data) != {"notes", "expenses"}:
                raise ValueError(
                    "Неизвестный формат старого JSON"
                )

            if (
                not isinstance(data["notes"], list)
                or not isinstance(data["expenses"], list)
            ):
                raise ValueError(
                    "notes и expenses должны быть списками"
                )

            items = [
                Note(text)
                for text in data["notes"]
            ]

            items += [
                Expense(row["amount"], row["category"])
                for row in data["expenses"]
            ]

        elif isinstance(data, list):
            items = []

            for row in data:
                if (
                    not isinstance(row, dict)
                    or row.get("type") not in self.MODEL_TYPES
                ):
                    raise ValueError(
                        "Неизвестный тип записи в JSON"
                    )

                model = self.MODEL_TYPES[row["type"]]
                item = model.from_dict(row)
                items.append(item)

        else:
            raise ValueError(
                "Ожидался список записей в JSON"
            )

        if len({item.id for item in items}) != len(items):
            raise ValueError(
                "В JSON повторяются id записей"
            )

        self._items = items
        return list(self._items)

    def add(self, item):
        if type(item) not in self.MODEL_TYPES.values():
            raise TypeError(
                "Ожидался BaseItem, Note, Reminder или Expense"
            )

        if any(
            existing.id == item.id
            for existing in self._items
        ):
            raise ValueError(
                "Запись с таким id уже существует"
            )

        self._items.append(item)

        try:
            self.save()
        except OSError:
            self._items.pop()
            raise

    def get_all(self, item_type):
        return [
            item
            for item in self._items
            if isinstance(item, item_type)
        ]

    def delete(self, item_id):
        for index, item in enumerate(self._items):
            if item.id == item_id:
                self._items.pop(index)

                try:
                    self.save()
                except OSError:
                    self._items.insert(index, item)
                    raise

                return True

        return False