from peewee import *

db = SqliteDatabase('tests.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    is_teachers = BooleanField()

    class Meta:
        database = db  
