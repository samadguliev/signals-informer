import datetime
from logger import logger
from peewee import Model, CharField, IntegerField, DateTimeField, AutoField
from database import db, get_db_connection


class BaseModel(Model):
    class Meta:
        database = db


class Test(BaseModel):
    username = CharField()
    age = IntegerField()

    @staticmethod
    def create_test(username, age):
        with get_db_connection():
            user = Test.create(username=username, age=age)
            return user


class Signal(BaseModel):
    id = AutoField()
    text = CharField()
    created = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def create_signals(signals) -> list['Signal']:
        with get_db_connection():
            with db.atomic():
                try:
                    signals_list: list[Signal] = [Signal(text=signal) for signal in signals]
                    Signal.bulk_create(signals_list)
                    return signals_list
                except BaseException as e:
                    logger.error(str(e))
                    return []

    @staticmethod
    def clear_table():
        with get_db_connection():
            with db.atomic():
                try:
                    delete_q = Signal.delete()
                    delete_q.execute()
                except BaseException as e:
                    logger.error(str(e))

    @staticmethod
    def get_all() -> list['Signal']:
        with get_db_connection():
            with db.atomic():
                try:
                    return Signal.select()
                except BaseException as e:
                    logger.error(str(e))
