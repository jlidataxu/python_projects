from flask import Flask, url_for, request, render_template, redirect, flash, make_response, session
import logging
import os
from logging.handlers import RotatingFileHandler
import pymysql

app = Flask(__name__)
# =======================
# 0.1 hello page, debug
# =======================
@app.route('/hello')
def hello_world():
	return 'Hello Beautiful World!!' 
# =======================
# 0.2 route: index page, userprofile,  post page
# =======================
# @app.route('/')
# def index():
# 	return 'Index Page'

# user profile page
@app.route('/user/<username>')
def show_userprofile(username):
	return 'User: %s'  % username

# post_id page 
@app.route('/post/<int:post_id>')
def show_postid(post_id):
	return 'Post_ID: %d' % post_id 

# =======================
# 0.3 url for
# =======================
@app.route('/show_url_for')
def show_url_for():
	return url_for('show_userprofile', username='jamesli')

# =======================
# 0.4 HTTP Methods
# GET: localhost:5000/login?username=jli&email=jli@datazoo.com
# POST: render request without explict url
# =======================
# @app.route('/login', methods=['GET', 'POST'])

# def login():
# 	if request.values:
# 		return 'username is %s' % request.values['username']
# 	else:
# 		return '<form method="get" action="/login"><input type="text" name="username"/><p><button type ="submit">Submit</button>'

# def login():
# 	if request.method == 'POST':
# 		return 'username is %s' % request.values['username']
# 	else:
# 		return '<form method="post" action="/login"><input type="text" name="username"/><p><button type ="submit">Submit</button>'


# =======================
# 0.5 templates
# 1) create login.html
# 2) add render_template method
# 3) add valid_log function
# =======================
@app.route('/login', methods=['GET', 'POST'])

def login():
	error = None
	if request.method == 'POST':
		if valid_login(request.form.get('username'),request.form.get('password')):
			# 0.6.1 redirect method
			# 0.7.1 flash: message
			flash("Succesfully logged in")
			# 1.0 coookie: 1) use response to set cookie
			# response = make_response(redirect(url_for('welcome')))
			# response.set_cookie('username', request.form.get('username'))
			# 1.1 session: 1) use session to get username
			session['username'] = request.form.get('username')
			return redirect(url_for('welcome'))
		else:
			error = "Incorrect username and password"
			# 1.4.2 logger: log warning for incorrect username
			app.logger.warning("Incorrect username or password for user %s" , request.form.get('username'))
	return render_template('login.html', error=error)

# 1.3.1 use mysql to validate password
def valid_login(username, password):
	MYSQL_DATABASE_HOST = os.getenv('IP', '0.0.0.0')
	MYSQL_DATABASE_USER = 'jlidataxu'
	MYSQL_DATABASE_DB = "my_flask_app" 
	MYSQL_DATABASE_PASSWORD = ""
	conn = pymysql.connect(
		host=MYSQL_DATABASE_HOST,
		user=MYSQL_DATABASE_USER,
		passwd=MYSQL_DATABASE_PASSWORD,
		db=MYSQL_DATABASE_DB
		)
	cursor = conn.cursor()
	count_sql = ("""select count(*) from user where username = '%s' and password = '%s' """  %(username, password))
	# print count_sql
	cursor.execute(count_sql)
	data = cursor.fetchone()
	if data:
		return True
	else:
		return False
 

# =======================
# 0.6 redirect
# 1) redirect in login page
# 2) create welcome page
# 3) create welcome.html template
# =======================
# 1.0 cookie: 2) update welcome function to use cookie to get username
@app.route('/')
def welcome():
	#username = request.cookies.get("username")
	# 1.1 session: 2) update welcome function
	if 'username' in session:
		return render_template('welcome.html', username=session['username'])
	else:
		return redirect(url_for('login'))

# 1.0 cookie: 3) add logout function
@app.route('/logout')
def logout():
	# response = make_response(redirect(url_for('login')))
	# response.set_cookie('username', '', expires=0)
	# 1.1 session: 3) update logout function
	session.pop('username', None)
	return redirect(url_for('welcome'))

# main method
if __name__ == '__main__':
	# turn on debug mode
	# 0.7.3 flash: add secret key
	app.secret_key = ']\xd9\xa6}\x82\xf3}\x82\x1f\xb3\x9e\x9d\xb0\xa7\x17\x7f\x0e6\xa8\x13\x8b\xb0]U'
	# 1.2 logger: 1) add hondler
	handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.debug = True
	# run app
	host = os.getenv('IP', '0.0.0.0')
	port = int(os.getenv('PORT', 5000))
	app.run(host=host,port=port)




