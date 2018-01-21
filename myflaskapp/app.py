# main file of application

from flask import Flask, render_template
from data import Articles

# create instance of flask app
app = Flask(__name__)

# to run in debug mode, let's you see changes in your application without having to restart the server
app.debug = True

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


# if this condition met this script will be executed
if __name__ == '__main__':
	app.run()

	# to run in debug mode, let's you see changes in your application without having to restart the server
	#app.run(debug=True)
