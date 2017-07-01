from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():

 
  return render_template('index.html')

@app.route('/about')
def contacts():

  return render_template('about.html')

@app.route('/test-list')
def testsList():

  return render_template('tests.html')  

@app.route('/registr')
def registr():

  return render_template('registr.html') 

@app.route('/login')
def login():

  return render_template('login.html')   

if __name__ == '__main__':
    app.run(debug=True)