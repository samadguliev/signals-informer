from peewee import Model, CharField, IntegerField, ForeignKeyField
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
