from peewee import Model, CharField, IntegerField, ForeignKeyField
from database import db


class BaseModel(Model):
    class Meta:
        database = db


class Test(BaseModel):
    username = CharField()
    age = IntegerField()
