from flask import render_template
from flask_blog import app
from author.form import RegisterForm

@app.route('/login')
def login():
    return "Hello, User!"

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    return render_template('author/register.html', form=form)