import bot
from database import db
from models import Test
from dotenv import load_dotenv

load_dotenv()


def initialize_db():
    db.connect()
    db.create_tables([Test])


def close_db():
    if not db.is_closed():
        db.close()


if __name__ == '__main__':
    initialize_db()
    bot.run_discord_bot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
