# main file of application

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
#from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# create instance of flask app
app = Flask(__name__)
# to run in debug mode, let's you see changes in your application without having to restart the server
app.debug = True


# configure mysql to work with application
app.config['MYSQL_HOST'] = 'localhost'   # where db is stored
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'   # so mysqldb knows to return data in dict form

# initialize database
mysql = MySQL(app)   # wrap up app variable


# read data from data.py
#Articles = Articles()

# create a route
@app.route('/')
def index():
	return render_template('home.html')


# create a route
@app.route('/about')
def about():
	return render_template('about.html')


# create a route
@app.route('/articles')
def articles():
	#return render_template('articles.html', articles=Articles)   # don't use same name for data and html variable, causes error
	# create cursor
	cur = mysql.connection.cursor()

	# get Articles
	result = cur.execute("SELECT * FROM articles")

	articles = cur.fetchall()   # returns all results in dictionary form

	if result > 0:
		return render_template('articles.html', articles=articles)
	else:
		msg = 'No articles found'
		return render_template('articles.html', msg=msg)


# create a route for article linke
@app.route('/article/<string:id>/')   # <> indicates a dynamic value
def article(id):
	# create cursor
	cur = mysql.connection.cursor()

	# get Articles
	result = cur.execute("SELECT * FROM articles WHERE id=%s", [id])

	article = cur.fetchone()   # returns all results in dictionary form

	return render_template('article.html', article=article)


# use a class to handle forms
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message="Passwords don't match")
	])
	confirm = PasswordField('Confirm password')

# user registration
@app.route('/register', methods=['GET', 'POST'])   # accepts both types of requests
def register():
	form = RegisterForm(request.form)   # class form created above

	# check if it's POST or GET requests
	if request.method == 'POST' and form.validate():

		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))	   # this needs to be encrypted before sending to db

		# create cursor
		cur = mysql.connection.cursor()

		# insert data (%s is string replace)
		cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)",
					(name, email, username, password))

		# commit to database
		mysql.connection.commit()

		# close connection
		cur.close()

		# flash message once registered
		flash('You are now registered and can log in', 'success')

		# return user to homepage
		return redirect(url_for('index'))

	return render_template('register.html', form=form)


# user login
@app.route('/login', methods=['GET', 'POST'])   # because we want to be able to receive both types of requests
def login():
	if request.method == 'POST':

		# get from fields
		username = request.form['username']
		password_candidate = request.form['password']

		# create cursor
		cur = mysql.connection.cursor()

		# get user by Username
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:   # if there's any rows found
			# get hash
			data = cur.fetchone()   # only fetches the first username matching username variable
			password = data['password']

			# compare Passwords
			if sha256_crypt.verify(password_candidate, password):
				#app.logger.info('PASSWORD MATCHED')   # how you log stuff to the bash console

				# create session variable if successful Login
				session['logged_in'] = True
				session['username'] = username # comes from the form

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))   # redirects to a different endpoint (python function)
			else:
				#app.logger.info('PASSWORD NOT MATCHED')
				error = 'Invalid password!'
				return render_template('login.html', error=error)

			# close connection (to database)
			cur.close()

		else:
			#app.logger.info('NO USER')
			error = 'Username not found!'
			return render_template('login.html', error=error)

	return render_template('login.html')   # this is rendered when you first go to this endpoint

# check if user logged in, this decorator can then be used an any route!!!!
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):   # this line means that all the arguments of original function should be returned
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, please log in.', 'danger')
			return redirect(url_for('login'))
	return wrap


# User logout
@app.route('/logout')
@is_logged_in   # wrapper that requires user to be logged in to access url
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('index'))

# dashboard
@app.route('/dashboard')
@is_logged_in   # wrapper that requires user to be logged in to access url
def dashboard():

	# create cursor
	cur = mysql.connection.cursor()

	# get Articles
	result = cur.execute("SELECT * FROM articles")

	articles = cur.fetchall()   # returns all results in dictionary form

	if result > 0:
		return render_template('dashboard.html', articles=articles)
	else:
		msg = 'No articles found'
		return render_template('dashboard.html')

	# close connection
	cur.close()

# use a class to add articles, used for adding and editing articles
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body = TextAreaField('Body', [validators.Length(min=30)])

# add article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in   # wrapper that requires user to be logged in to access url
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data

		# create cursor
		cur = mysql.connection.cursor()

		# execute
		cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",
			(title, body, session['username']))

		# commit changes to db
		mysql.connection.commit()

		# close cursor
		cur.close()

		flash('Article created', 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_article.html', form=form)

# if this condition met this script will be executed
if __name__ == '__main__':

	app.secret_key = 'secret123'
	app.run()

	# to run in debug mode, let's you see changes in your application without having to restart the server
	#app.run(debug=True)
