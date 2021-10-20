from flask import Flask,render_template
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
def create_app():
    app = ...
    # existing code omitted

    from . import db
    db.init_app(app)

    return app
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


#

# @app.route("/login", methods=["GET", "POST"])
# def login():
    # """Log user in"""

    # # Forget any user_id
    # session.clear()

    # # User reached route via POST (as by submitting a form via POST)
    # if request.method == "POST":

    #     # Ensure username was submitted
    #     if not request.form.get("Username"):
    #         return apology("Must provide username", 403)

    #     # Ensure password was submitted
    #     elif not request.form.get("Password"):
    #         return apology("Must provide password", 403)

    #     # Query database for username
    #     user_rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("Username"))
    #     pass_rows = 
    #     # Query database for password
    #     # rows = db.execute("SELECT * FROM passwords WHERE password = ?", request.form.get("Password"))

    #     # Ensure username exists and password is correct
    #     if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
    #         return apology("invalid username and/or password", 403)

    #     # Remember which user has logged in
    #     session["user_id"] = rows[0]["id"]

    #     # Redirect user to home page
    #     return redirect("/")

    # # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("login.html")




#
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
def creaateRegisterPage():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)