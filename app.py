from flask import Flask
from flask import render_template, request, redirect, url_for
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bootstrap import BOOTSTRAP_VERSION, Bootstrap

from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import pytz
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/bin/python3")
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))
    mail_address = db.Column(db.String(50), nullable=False, unique=True)
    login_session = db.Column(db.Boolean)
    icon_path = db.Column(db.String)
    API_KEY = db.Column(db.Integer)

class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    registered_on = db.Column(db.DateTime)
    user_id1 = db.Column(db.Integer, default='0')
    user_id2 = db.Column(db.Integer, default='0')
    user_id3 = db.Column(db.Integer, default='0')
    user_id4 = db.Column(db.Integer, default='0')
    user_id5 = db.Column(db.Integer, default='0')

class schedules(db.Model):
    schedules_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, default='0')
    started_at = db.Column(db.DateTime)
    memo = db.Column(db.String, default='0')
    is_deleted = db.Column(db.Boolean, default=False)
    registerd_on = db.Column(db.DateTime)
    group_id = db.Column(db.Integer)

class Joins(db.Model):
    join_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    is_joined = db.Column(db.Boolean, default=False)

class Follows(db.Model):
    follow_id = db.Column(db.Integer, primary_key=True)
    follow_userId = db.Column(db.Integer)
    follower_userId = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/', methods=['GET', 'POST'])
# @login_required
# def index():
#     if request.method == 'GET':
#         posts = Post.query.all()
#         return render_template('home.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/")
def createHomePage():
    return render_template("home.html")

@app.route("/login")
def createLoginPage():
    return render_template("login.html")

@app.route("/list")
def createListPage():
    return render_template("list.html")

@app.route("/friend")
def createFriendPage():
    return render_template("friend.html")

@app.route("/mypage")
def createMyprofilePage():
    return render_template("mypage.html")

@app.route("/register")
def createRegisterPage():
    return render_template("register.html")

@app.route("/layout")
def test():
    return render_template("layout.html")