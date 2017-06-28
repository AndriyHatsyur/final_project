from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
	conn = sqlite3.connect('project.db')
	print "Opened database successfully";

	conn.execute('''CREATE TABLE COMPAfffNY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50) ,
       SALARY         REAL);''')
	print "Table created successfully";

	conn.close()
    #return render_template('index.html')

@app.route('/contacts')
def contacts():
    return 'contact'

if __name__ == '__main__':
    app.run()