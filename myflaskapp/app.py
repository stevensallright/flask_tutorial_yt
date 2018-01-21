# main file of application

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

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
Articles = Articles()

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
	return render_template('articles.html', articles=Articles)   # don't use same name for data and html variable, causes error


# create a route for article linke
@app.route('/article/<string:id>/')   # <> indicates a dynamic value
def article(id):
	return render_template('article.html', id=id)


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

# route for form class above
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



# if this condition met this script will be executed
if __name__ == '__main__':

	app.secret_key = 'secret123'
	app.run()

	# to run in debug mode, let's you see changes in your application without having to restart the server
	#app.run(debug=True)
