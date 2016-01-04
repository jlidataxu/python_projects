# flaskapp0.2 flask model test
from flask_blog import db 
from author.models import *
db.create_all() 
author = Author('james li', 'zliyclj1@gmail.com', 'james','123456', True)
db.session.add(author)
db.session.commit()
author = Author('jorge k', 'jorge@gmail.com', 'jorge','123456', True)
db.session.add(author)
db.session.commit()
authors = Author.query.all()
authors
authors[1].fullname
authors = Author.query.filter_by(username='jorge').first()
authors

# drop all tables
from flask_blog import db 
from author.models import *
db.session.commit()
db.drop_all()