from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    EmptyForm,
    PostForm,
    RequestPasswordResetForm,
    ResetPasswordForm,
)
from app.models import User, Post
from app.email import send_password_reset_email

# Step 52 in the Workflow
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# methods=[] part is the step 75 in the Workflow
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required  # step 37 in the workflow
def index():

    # step 75 in the Workflow
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You post has been submitted")

        # POST/redirect/GET pattern
        return redirect(url_for("index"))

    # user = {"username": "Babalu"}
    # posts = [
    #     {"author": {"username": "Scar"}, "body": "Mufasani man oldirganman"},
    #     {"author": {"username": "Shrek"}, "body": "Shut up, you stupid donkey!"},
    # ]

    # step 75 in the Workflow
    # posts = current_user.followed_posts().all()

    # step 83 in the Workflow - modify the step 75
    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    # step 85 in the Workflow
    next_url = url_for("index", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("index", page=posts.prev_num) if posts.has_prev else None
    return render_template(
        "index.html",
        title="Home",
        posts=posts.items,
        form=form,
        next_url=next_url,
        prev_url=prev_url,
    )  # read the step 39


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
        if not next_page or url_parse(next_page).netloc != "":
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
    # posts = [
    #     {"author": user, "body": "Test post #1"},
    #     {"author": user, "body": "Test post #2"},
    # ]

    # step 87 in the Workflow
    page = request.args.get("page", 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    next_url = (
        url_for("user", username=user.username, page=posts.next_num)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for("user", username=user.username, page=posts.prev_num)
        if posts.has_prev
        else None
    )

    # step 72 in the Workflow
    form = EmptyForm()

    return render_template(
        "user.html",
        user=user,
        posts=posts.items,
        form=form,
        next_url=next_url,
        prev_url=prev_url,
    )


# Step 53 in the Workflow
@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # we skip the else clause that is POST request with validation errors
    return render_template("edit_profile.html", title="Edit Profile", form=form)


# Workflow step 69-70, imported EmptyFrom from app.forms
@app.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} is not found!")
            return redirect(url_for("index"))
        if user == current_user:
            flash("You can not follow yourself")
            return redirect(url_for("user", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f"You are now following {username}")
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("index"))


@app.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} is not found!")
            return redirect(url_for("index"))
        if user == current_user:
            flash("You can not unfollow yourself")
            return redirect(url_for("user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"You have unfollowed {username}")
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("index"))


# step 77 in the Workflow
@app.route("/explore")
@login_required
def explore():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()

    # step 83 in the Workflow - modify the posts variable
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    # step 85 in the Workflow
    next_url = url_for("explore", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("explore", page=posts.prev_num) if posts.has_prev else None
    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


# Step 94 in the workflow
@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Instructions were sent. Please check your inbox.")
        return redirect(url_for("login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


# step 100 in the Wokflow
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    user = User.verify_reset_password(token)
    if not user:
        return redirect(url_for("index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset successfully")
        return redirect(url_for("login"))

    return render_template("reset_password.html", form=form)

