from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Babalu"}
    posts = [
        {"author": {"username": "Mufasa"}, "body": "Mufasani man oldirganman"},
        {"author": {"username": "Shrek"}, "body": "Shut up, you stupid donkey!"},
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    # First we check if already logged in user is trying to login again by mistake
    # If true, we will just redirect them to the main page
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        # We will query the User database and get the first row
        user = User.query.filter_by(username=form.username.data).first()

        # if this user does not exist or password check return incorrect hash
        # we will flash a message that something is wrong
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # Otherwise, we will log them in
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign in", form=form)


# Function to handle logging users out. Step 33 in the Workflow
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
