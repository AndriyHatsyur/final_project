from peewee import *

db = SqliteDatabase('tests.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db  


class Test(Model):
    name = CharField(unique=True)
    description = CharField()
    user = ForeignKeyField(User, related_name='user')

    class Meta:
        database = db 

class Questions(Model):
    description = CharField()
    score = IntegerField()
    answer = IntegerField()
    test = ForeignKeyField(Test, related_name='test')

    class Meta:
        database = db 

class Answer(Model):
    description = CharField()
    number = IntegerField()
    questions = ForeignKeyField(Questions, related_name='questions')

    class Meta:
        database = db         
 
