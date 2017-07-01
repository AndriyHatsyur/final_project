from flask import Flask, request, session, render_template, redirect, url_for
import hashlib
from model import *

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():

 
  return render_template('index.html')

@app.route('/about')
def contacts():

  return render_template('about.html')

@app.route('/test-list')
def testsList():

  return render_template('tests.html')  

#user registration
@app.route('/registr', methods=["GET", "POST"])
def registr():

	error = None

	if request.method == "POST":

		if not request.form.get("username"):
			error = 'must provide username'

		elif not request.form.get("email"):
			error = 'must provide email'

		elif not request.form.get("password"):
			error = 'must provide password'

		elif not request.form.get("repeat_password"):
			error = 'must provide password again'

		elif request.form.get("password") != request.form.get("repeat_password"):
        	 error = "passwords don`t match" 			
		
		if error == None:
			try:
				pas = hashlib.md5(request.form.get("password"))
				p_hash = pas.hexdigest()

				user = User.create(username = request.form.get("username"),\
									email = request.form.get("email"),\
									password = p_hash,\
									is_teachers = 0)
				user.save()
				session["username"] = request.form.get("username")
				return redirect(url_for('user', username=request.form.get("username")))
			except:	
		    	 error = "username or email already exists" 

	return render_template('registr.html', error=error) 

@app.route('/login')
def login():

  return render_template('login.html')   

@app.route('/user/<username>')
def user(username):  

	return username

if __name__ == '__main__':
    app.run(debug=True)
