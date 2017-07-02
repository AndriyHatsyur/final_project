from flask import Flask, request, session, render_template, redirect, url_for, jsonify
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
	tests = Test.select()
	return render_template('testsList.html', tests=tests)  

#user registration
@app.route('/registr', methods=["GET", "POST"])
def registr():

	error = None

	if request.method == "POST":

		if not request.form.get("username"):
			error = 'Must provide username'

		elif not request.form.get("email"):
			error = 'Must provide email'

		elif not request.form.get("password"):
			error = 'Must provide password'

		elif not request.form.get("repeat_password"):
			error = 'Must provide password again'

		elif request.form.get("password") != request.form.get("repeat_password"):
        	 error = "Passwords don`t match" 			
		
		if error == None:
			try:
				pas = hashlib.md5(request.form.get("password"))
				p_hash = pas.hexdigest()

				user = User.create(username = request.form.get("username"),\
									email = request.form.get("email"),\
									password = p_hash)
				user.save()
				session["user_id"] = user.id
				session["user_name"] = user.username
				return redirect(url_for('user', username=user.username))
			except:	
		    	 error = "Username or email already exists" 

	return render_template('registr.html', error=error) 

@app.route('/login', methods=["GET", "POST"])
def login():

	error = None

	if request.method == "POST":

		if not request.form.get("username"):
			error = 'Must provide username'

		elif not request.form.get("password"):
			error = 'Must provide password'

		if error == None:
			try:
				pas = hashlib.md5(request.form.get("password"))
				p_hash = pas.hexdigest()

				user = User.get(User.username == request.form.get("username"))
				
				if p_hash == user.password:

					session["user_id"] = user.id
					session["user_name"] = user.username
					return redirect(url_for('user', username=user.username))

				else:
					error = "Wrong password"
			except:	
		    	 error = "Wrong username"

	return render_template('login.html',error=error)   

@app.route('/user/<username>', methods=["GET", "POST"])
def user(username):  

	if not 'user_id' in session:
		return redirect(url_for("login"))

	user = User.get(User.id == session["user_id"])

	message = None
	error = None

	if request.form.get("email") and request.form.get("password"):

		pas = hashlib.md5(request.form.get("password"))
		p_hash = pas.hexdigest()

		if p_hash == user.password:
			user.email = request.form.get("email")
			user.save()
			message = 'Email changed'
		else:
	
			error = 'Wrong password'	

	if request.form.get("old_password") and request.form.get("new_password") and request.form.get("repeat_password"):
		if request.form.get("new_password") != request.form.get("repeat_password"):
			error = "Passwords don`t match"
		else:
			
			pas = hashlib.md5(request.form.get("old_password"))
			p_hash = pas.hexdigest()

			if p_hash == user.password:
				pas = hashlib.md5(request.form.get("new_password"))
				p_hash = pas.hexdigest()
				user.password = p_hash
				user.save()
				message = 'Password changed'
			else:
		
				error = 'Wrong password'

	return render_template('user.html', user=user, message=message, error=error)   

@app.route("/logout")
def logout():
    
    session.clear()

    return redirect(url_for("login"))


@app.route('/create-test/<test>', methods=["GET", "POST"])
def createTest(test):
	if not 'user_id' in session:

		return redirect(url_for("login"))

	error = None

	if request.method == "POST":

		if test == 'new':

			if not request.form.get("testName"):
				error = 'Must provide name of test'

			if not request.form.get("testDescription"):
				error = 'Must provide description of test'

			if error == None:
				user = User.get(User.id == session["user_id"])

				test = Test.create(name = request.form.get("testName"),\
									description = request.form.get("testDescription"),\
									user = user)
				test.save()	

				return redirect(url_for('createTest', test=test.name, q=1))

		else:

			if error == None:

				test = Test.get(Test.name == test)

				question = Questions.create(number = request.args.get("q"),\
											description = request.form.get("question"),\
											score = request.form.get("score"),\
											answer = request.form.get("answer"),\
											test = test)
				question.save()

				for i in range(1,5):
					answer = Answer.create(description = request.form.get("answer"+str(i)),\
											number = i,\
											questions = question)

				return redirect(url_for('createTest', test=test.name, q=int(request.args.get("q"))+1))

	return render_template('createTest.html',error=error)   


@app.route('/test/<name>', methods=["GET", "POST"])
def startTest(name):
   
    test = Test.get(Test.name == name)
    question = Questions.select().where(Questions.test == test, Questions.number == request.args.get("q"))

    count = Questions.select().where(Questions.test == test).count()

    if int(request.args.get("q")) > count:

    	return redirect(url_for('result', test=test.name))


    if request.form.get("answer"):
    	score = 0

    	if int(request.form.get("answer")) == question[0].answer:
    		score = question[0].score

    	history = History.create(test = test.id,\
    							 questions = question[0].id,\
    							 answer = score,\
    							 user = session["user_id"])
    	history.save()

    	return redirect(url_for('startTest', name=test.name, q=int(request.args.get("q"))+1))

    return render_template('startTest.html',question=question, test=test)



@app.route('/result/<test>', methods=["GET", "POST"])
def result(test):

	test = Test.get(Test.name == test)

	history = History.select().where(History.test == test.id, History.user == session["user_id"] )

	return render_template('result.html', test=test , history=history)

if __name__ == '__main__':
    app.run(debug=True)
