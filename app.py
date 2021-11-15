from flask import Flask
from flask import render_template, request, redirect, url_for, session
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
import datetime
import pytz
from datetime import timedelta
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(minutes=5) # -> 5分 #(days=5) -> 5日保存

class User(UserMixin, db.Model):
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

class Schedules(db.Model):
    schedules_id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime)
    place = db.Column(db.String, default='0')
    event_name = db.Column(db.String, default='0')
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
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        mailaddress = request.form.get('mail_address')

        user = User(username=username, password=generate_password_hash(password, method='sha256'), mail_address=mailaddress)

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if check_password_hash(user.password, password):
            user.login_session = True
            db.session.commit()
            # セッションにユーザーネームを保存
            session["user"] = user.username
            login_user(user)
            return redirect('/home')
    else:
        if "user" in session:
            return render_template("home.html")
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    username = session["user"]
    user = User.query.filter_by(username=username).first()
    user.login_session = False
    db.session.commit()
    session.pop("user", None)
    logout_user()
    return redirect('/')

@app.route("/home", methods=['POST'])
@login_required
def addSchedule():
    if request.method == 'POST':
        date_tmp = request.form.get('date')
        place = request.form.get('place')
        event = request.form.get('event')
        print(date_tmp)
        date =  datetime.datetime.strptime(date_tmp, '%Y-%m-%dT%H:%M')
        print(date)
        schedule = Schedules(started_at=date, place=place, event_name=event)

        db.session.add(schedule)
        db.session.commit() 
        return render_template("home.html")
    else:
        return redirect('home.html')
@app.route("/mypage", methods=["GET", "POST"])
@login_required
def editMyProfile():
    if request.method == "POST":
        username = request.form.get("user_name")
        mail_address = request.form.get("mail_address")
        password = request.form.get("password")
        icon = request.form.get("icon")
        user = User(username=username, mail_address=mail_address, password=password, icon_path=icon)
        db.session.add(user)
        db.session.commit()
        return render_template("mypage.html")
    else:
        return render_template("mypage.html")
@app.route("/home")
@login_required
def createHomePage():
    return render_template("home.html")

@app.route("/)
def createLoginPage():
    return render_template("login.html")

@app.route("/list")
def createListPage():
    return render_template("list.html")

@app.route("/friend")
def createFriendPage():
    return render_template("friend.html")

@app.route("/mypage")
@login_required
def createMyprofilePage():
    return render_template("mypage.html")

@app.route("/register")
@login_required
def createRegisterPage():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True,host='localhost',port=5000)
