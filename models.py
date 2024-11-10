import datetime
from logger import logger
from peewee import Model, CharField, DateTimeField, AutoField, BigIntegerField
from database import db, get_db_connection


class BaseModel(Model):
    class Meta:
        database = db


class Signal(BaseModel):
    id = AutoField()
    channel = BigIntegerField()
    created = DateTimeField(default=datetime.datetime.now)
    text = CharField()

    @staticmethod
    def create_signals(signals, channel: int) -> list['Signal']:
        with get_db_connection():
            with db.atomic():
                try:
                    signals_list: list[Signal] = [Signal(text=signal, channel=channel) for signal in signals]
                    Signal.bulk_create(signals_list)
                    return signals_list
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
    def get_all(channel: int) -> list['Signal']:
        with get_db_connection():
            with db.atomic():
                try:
                    return Signal.select().where(Signal.channel == channel)
                except BaseException as e:
                    logger.error(str(e))
