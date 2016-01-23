from flask import render_template, redirect, url_for, request, session, flash
from flask_blog import app
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
        
    if request.method == 'POST' and form.validate():
        author = Author.query.filter_by(
            username=form.username.data
            ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username']=form.username.data
                session['is_author']=author.is_author
                flash("User %s logged in" % form.username.data)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else: 
                error = "incorrect username or password"
        else: 
            error = "incorrect username or password"
    return render_template('author/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)
    
@app.route('/success')
def success():
    return "Author registered!"
    
@app.route('/login_success')
@login_required
def login_success():
    return "Author login!"
    
@app.route('/logout')
def logout():
    session.pop('username')
    flash("User logged out")
    return redirect(url_for('index'))