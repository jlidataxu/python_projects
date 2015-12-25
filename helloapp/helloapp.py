from flask import Flask
app = Flask(__name__)

# index page
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
# hello page
@app.route('/hello')
def hello_world():
	return 'Hello Beautiful World!!' 

# main method
if __name__ == '__main__':
	# turn on debug mode
	app.debug = True
	# run app
	app.run()