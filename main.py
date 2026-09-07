from pathlib import Path

from bot import BotController
from storage import Storage


if __name__ == "__main__":
    storage = Storage(Path(__file__).with_name("data.json"))
    bot = BotController(storage)
    bot.run()