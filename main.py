import bot
from database import db
from models import Test
from dotenv import load_dotenv
from logger import logger

load_dotenv()


def initialize_db():
    try:
        db.connect()
        db.create_tables([Test])
        logger.info("Success connection")
    except BaseException as e:
        logger.error("Initializing error: " + str(e))


def close_db():
    if not db.is_closed():
        db.close()


if __name__ == '__main__':
    initialize_db()
    bot.run_discord_bot()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
