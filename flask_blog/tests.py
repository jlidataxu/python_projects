# set path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

from flask_blog import app, db

# models
from author.models import *
from blog.models import *

class UserTest(unittest.TestCase):
    def setUp(self):
        db_username = app.config['DB_USERNAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        self.db_url = "mysql+pymysql://%s:%s@%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['BLOG_DATABASE_NAME'] = 'test_blog'
        app.config["SQLALCHEMY_DATABASE_URI"] = self.db_url + app.config['BLOG_DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_url)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("CREATE DATABASE " + app.config['BLOG_DATABASE_NAME'])
        db.create_all()
        conn.close()
        self.app = app.test_client()
        
    def tearDown(self):
        db.session.remove()db
        engine = sqlalchemy.create_engine(self.db_url)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("DROP DATABASE " + app.config['BLOG_DATABASE_NAME'])
        conn.close()