import datetime
from logger import logger
from peewee import Model, CharField, DateTimeField, AutoField, BigIntegerField, DoubleField
from database import db, get_db_connection
from peewee import JOIN


class BaseModel(Model):
    class Meta:
        database = db


class Signal(BaseModel):
    id = AutoField()
    channel = BigIntegerField()
    currency_code = CharField()
    text = CharField()
    created = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def create_signals(signals) -> list['Signal']:
        with get_db_connection():
            with db.atomic():
                try:
                    Signal.bulk_create(signals)
                    return signals
                except BaseException as e:
                    logger.error(str(e))
                    return []

    @staticmethod
    def clear_table(channel: int):
        with get_db_connection():
            with db.atomic():
                try:
                    delete_q = Signal.delete().where(Signal.channel == channel)
                    delete_q.execute()
                except BaseException as e:
                    logger.error(str(e))

    @staticmethod
    def get_by_channel(channel: int) -> list['Signal']:
        with get_db_connection():
            try:
                return Signal.select(Signal, Currency).where(Signal.channel == channel).join(Currency, on=(Signal.currency_code == Currency.code), join_type=JOIN.INNER)
            except BaseException as e:
                logger.error(str(e))

    @staticmethod
    def get_all() -> list['Signal']:
        with get_db_connection():
            try:
                return Signal.select()
            except BaseException as e:
                logger.error(str(e))


class Currency(BaseModel):
    id = AutoField()
    code = CharField()
    price = DoubleField()

    @staticmethod
    def get_existing_currencies() -> dict[str, 'Currency']:
        with get_db_connection():
            with db.atomic():
                try:
                    currencies = Currency.select()
                    return {currency.code: currency for currency in currencies}
                except BaseException as e:
                    logger.error(str(e))

    @staticmethod
    def create_currencies(currencies) -> list['Currency']:
        with get_db_connection():
            with db.atomic():
                try:
                    Currency.bulk_create(currencies)
                    return currencies
                except BaseException as e:
                    logger.error(str(e))

    @staticmethod
    def update_currencies(currencies) -> list['Currency']:
        with get_db_connection():
            with db.atomic():
                try:
                    Currency.bulk_update(currencies, fields=[Currency.price])
                    return currencies
                except BaseException as e:
                    logger.error(str(e))

