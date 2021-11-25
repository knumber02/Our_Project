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
from werkzeug.utils import secure_filename
import secrets
from PIL import Image
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.secret_key = 'user'
app.permanent_session_lifetime = timedelta(
    minutes=5)  # -> 5分 #(days=5) -> 5日保存

UPLOAD_FOLDER = './static/up'
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    group_name = db.Column(db.String(12))
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

# def allwed_file(filename):
#     # .があるかどうかのチェックと、拡張子の確認
#     # OKなら１、だめなら0
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        user = User(username=username, password=generate_password_hash(
            password, method='sha256'), mail_address=mailaddress)

        db.session.add(user)
        db.session.commit()
        return redirect('/')
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
            # セッションにユーザーidを保存
            session["user"] = user.id
            login_user(user)
            return redirect('/home')
    else:
        if "user" in session:
            return render_template("home.html")
        return render_template('login.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    id = session["user"]
    user = User.query.filter_by(id=id).first()
    user.login_session = False
    db.session.commit()
    session.pop("user", None)
    logout_user()
    return redirect('/')


@app.route("/home", methods=['POST'])
@login_required
def addSchedule():
    if request.method == 'POST':
        group = request.form.get("group")
        date_tmp = request.form.get('date')
        place = request.form.get('place')
        event = request.form.get('event')
        date = datetime.datetime.strptime(date_tmp, '%Y-%m-%dT%H:%M')
        schedule = Schedules.query.filter_by(group_id=group).first()
        if date:
            schedule.registerd_on = date
        if place:
            schedule.place = place
        if event:
            schedule.event = event

        # セッションにスケジュール情報を入力
        # session["schedule"] = schedule.schedules_id
        eventName = schedule.event_name
        db.session.add(schedule)
        db.session.commit()
        return render_template("home.html", event_name=eventName)
    else:
        # schedule_id = session["schedule"]
        # schedule = Schedules.query.filter_by(schedule_id=schedule_id).first()
        # eventName = schedule.event_name

        return render_template('home.html', event_name=eventName)


@app.route("/mypage", methods=["GET", "POST"])
@login_required
def editMyProfile():
    if request.method == "POST":
        username = request.form.get("username")
        mail_address = request.form.get("mail_address")
        password = request.form.get("password")
        # icon = request.form.get("icon")
        file = request.files["uploadFile"]
        filename = file.filename
        id = session["user"]
        user = User.query.filter_by(id=id).first()
        if username:
            user.username = username
        if mail_address:
            user.mail_address = mail_address
        if password:
            user.password = generate_password_hash(password, method='sha256')
        if file:
            user.icon_path = filename
            # 縮小して保存
            i = Image.open(file)
            i.thumbnail((200, 200))
             # ファイルの保存
            i.save(os.path.join(UPLOAD_FOLDER, filename))
        icon_path = user.icon_path
        currentUsername = user.username
        currentMail_address = user.mail_address
        db.session.add(user)
        db.session.commit()
        return render_template("mypage.html", img_file=icon_path, username=currentUsername, mail_address=currentMail_address)
    else:
        id = session["user"]
        user = User.query.filter_by(id=id).first()
        icon_path = user.icon_path
        username = user.username
        mail_address = user.mail_address
        return render_template("mypage.html", img_file=icon_path, username=username, mail_address=mail_address)


@app.route("/list", methods=["GET", "POST"])
@login_required
def createGroup():
    if request.method == "POST":
        group_name = request.form.get("group")
        date = datetime.datetime.today()
       
        group = Groups.query.filter_by(group_name=group_name, registerd_on=date, )
        return render_template("list.html", )
    else:
        id = session["user"]
        # フォローテーブルからユーザーのフォローしている友達全員の情報を取る
        follow_users = Follows.query.filter_by(follow_userId=id).all()
        #友達が１人でもいる場合
        if follow_users:
            arrFriends = []
            for follow_user in follow_users:
                follow_user_info = User.query.filter_by(id=follow_user.follower_userId).first()
                arrFriends.append(follow_user_info)
            return render_template("list.html",friends=arrFriends)
        else:
            return render_template("list.html")


@app.route("/search_friend", methods=["GET", "POST"])
@login_required
def search_friend():
    if request.method == "POST":
        # メールアドレス検索で友達追加する
        id = session["user"]
        searched_friend_mail = request.form.get("friend_mail")
        searched_friend = User.query.filter_by(mail_address=searched_friend_mail).first()
        searched_friend_icon = searched_friend.icon_path
        searched_friend_username = searched_friend.username
        searched_friend_id = searched_friend.id
        session["friend"] = searched_friend_id
        follow_check = Follows.query.filter_by(follow_userId=id, follower_userId=searched_friend_id).first()
        if follow_check:
            error_message = "この友達はすでに追加されています"
            return render_template("search_friend_check.html", error_message=error_message, searched_friend_username=searched_friend_username, searched_friend_icon=searched_friend_icon)
        else:
            return render_template("search_friend_check.html", searched_friend_username=searched_friend_username, searched_friend_icon=searched_friend_icon)
    else:
        return render_template("search_friend.html")
@app.route("/search_friend/check", methods=["POST", "GET"])
@login_required
def add_friend():
    if request.method == "POST":
        id = session["user"]
        searched_friend_id = session["friend"]
        follow = Follows(follow_userId=id, follower_userId=searched_friend_id)
        db.session.add(follow)
        db.session.commit()
        session.pop("friend", None)
        return redirect(url_for("createGroup"))
    if request.method == "GET":
        return render_template("search_friend_check.html")


@app.route("/home")
@login_required
def createHomePage():
    return render_template("home.html")

@app.route("/")
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
def createRegisterPage():
    return render_template("register.html")

@app.route("/search_friend")
def createSearchFriendPage():
    return render_template("search_friend.html")


if __name__ == "__main__":
    app.run(debug=True,host='localhost',port=5000)
