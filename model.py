from peewee import *

db = SqliteDatabase('tests.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db  

    def __iter__(self):
        yield 'username', self.username
        yield 'email', self.email  
           


class Test(Model):
    name = CharField(unique=True)
    description = CharField()
    user = ForeignKeyField(User, related_name='tests')

    class Meta:
        database = db 

    def __iter__(self):
        yield 'name', self.name
        yield 'description', self.description

        

class Questions(Model):
    number = IntegerField()
    description = CharField()
    score = IntegerField()
    answer = IntegerField()
    test = ForeignKeyField(Test, related_name='questions')

    class Meta:
        database = db

    def __iter__(self):
        yield 'number', self.number
        yield 'description', self.description  
        yield 'score', self.score
        yield 'answer', self.answer
        yield 'answers', [dict(an) for an in self.answers]
        
             

class Answer(Model):
    description = CharField()
    number = IntegerField()
    questions = ForeignKeyField(Questions, related_name='answers')

    class Meta:
        database = db         
 
    def __iter__(self):
        yield 'description', self.description  
        yield 'number', self.number

class History(Model):
    test = IntegerField()
    questions = IntegerField()
    answer = IntegerField()
    user = IntegerField()

    class Meta:
        database = db 

#History.create_table()
#Questions.create_table()
#Answer.create_table()