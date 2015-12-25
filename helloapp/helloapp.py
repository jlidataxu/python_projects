from flask import Flask, url_for, request, render_template, redirect
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
@app.route('/')
def index():
	return 'Index Page'

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
			return redirect(url_for('welcome', username=request.form.get('username')))
		else:
			error = "Incorrect username and password"
	return render_template('login.html', error=error)

def valid_login(username, password):
	if(username == password):
		return True
	else:
		return False

# =======================
# 0.6 redirect
# 1) redirect in login page
# 2) create welcome page
# 3) create welcome.html template
# =======================
@app.route('/welcome/<username>')

def welcome(username):
	return render_template('welcome.html', username=username)

# main method
if __name__ == '__main__':
	# turn on debug mode
	app.debug = True
	# run app
	app.run()




