from app import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route("/")
@app.route("/index")
@login_required  # step 37 in the workflow
def index():
    user = {"username": "Babalu"}
    posts = [
        {"author": {"username": "Mufasa"}, "body": "Mufasani man oldirganman"},
        {"author": {"username": "Shrek"}, "body": "Shut up, you stupid donkey!"},
    ]
    return render_template("index.html", title="Home", posts=posts)  # read the step 39


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
        # Step 36 in the Workflow
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page) != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


# Function to handle logging users out. Step 33 in the Workflow
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    # First we check if the user already logged in
    # If so, we will redirect the user to main page
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    # We will get the form from forms.py
    form = RegistrationForm()
    if form.validate_on_submit():
        # User's data passes all the validations
        # We will add it to User class
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Once the user is created, we will add him/her to our db
        db.session.add(user)
        db.session.commit()
        flash("Congratulations. You are not a registered user!")
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]

    return render_template("user.html", user=user, posts=posts)
