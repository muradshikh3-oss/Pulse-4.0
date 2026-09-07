from models import Expense, Note
from storage import Storage


class BotController:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def handle_note(self, update, context):
        message = update.effective_message

        if message is None:
            return

        text = " ".join(context.args or []).strip()

        if not text:
            await message.reply_text(
                "Использование: /note текст"
            )
            return

        note = Note(text)

        self.storage.add(note)

        await self._reply(
            message,
            f"Заметка добавлена: {note}",
        )

    async def handle_notes(self, update, context):
        message = update.effective_message

        if message is None:
            return

        notes = self.storage.get_all(Note)

        if not notes:
            await message.reply_text(
                "Заметок пока нет."
            )
            return

        lines = [
            f"{index}. {note}"
            for index, note in enumerate(notes, 1)
        ]

        await self._reply(
            message,
            "\n".join(lines),
        )

    async def handle_expenses(self, update, context):
        message = update.effective_message

        if message is None:
            return

        args = context.args or []

        if args:
            if len(args) < 2:
                await message.reply_text(
                    "Использование: /expenses 150 еда"
                )
                return

            try:
                amount = args[0].replace(",", ".")
                category = " ".join(args[1:])

                expense = Expense(amount, category)

            except ValueError:
                await message.reply_text(
                    "Укажи сумму больше нуля и категорию: "
                    "/expenses 150 еда"
                )
                return

            self.storage.add(expense)

            await self._reply(
                message,
                f"Расход добавлен: {expense}",
            )
            return

        expenses = self.storage.get_all(Expense)

        if not expenses:
            await message.reply_text(
                "Расходов пока нет."
            )
            return

        lines = [
            f"{index}. {expense}"
            for index, expense in enumerate(expenses, 1)
        ]

        total = sum(
            expense.amount
            for expense in expenses
        )

        lines.append(f"Итого: {total:.2f} ₽")

        await self._reply(
            message,
            "\n".join(lines),
        )

    async def _reply(self, message, text):
        part = ""
        units = 0

        for char in text:
            size = len(char.encode("utf-16-le")) // 2

            if units + size > 4000:
                await message.reply_text(part)
                part = ""
                units = 0

            part += char
            units += size

        if part:
            await message.reply_text(part)

    def run(self):
        from telegram.ext import Application, CommandHandler

        from config import TOKEN

        app = Application.builder().token(TOKEN).build()

        app.add_handler(
            CommandHandler("note", self.handle_note)
        )

        app.add_handler(
            CommandHandler("notes", self.handle_notes)
        )

        app.add_handler(
            CommandHandler("expenses", self.handle_expenses)
        )

        print("Бот запущен. Для остановки нажми Ctrl+C.")

        app.run_polling()