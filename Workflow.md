# Workflow

**SET UP**
- virtualenv, pip install libraries
- app folder: __init.py__ - instantiate app, import routes
- - templates folder: base, index html
- microblog.py: import app
- .flaskenv: FLASK_RUN, FLASK_ENV, FLASK_DEBUG
- config.py: Config class
- .gitignore: config.py, vscode settings, pycache, venv

**Step by step**

1. Create a directory
2. Make a virtual environment
3. Install libraries ( flask, python-dotenv, flask-wft... )

_______

4. Create "App" folder
    4.1 Create __init__.py inside "App" folder
        4.1.1 Import, instantiate Flask object (__name__ inside of it), import routes from app
    4.2 Create routes.py inside "App" folder
        4.2.1 Import app from App
        4.2.2 define @app.route and subsequent functions
    4.3 Create "Templates" folder inside
        4.3.1 Create "index.html" and "base.html"
        4.3.2 Index (and any further html files) will inherit from the Base using Jinja templates using {% block content %}{% endblock%}

_______

5. Create "microblog.py" (top level app) on the top level directory
    5.1 Import the app inside

6. Create ".flaskenv" file and put FLASK_APP=microblog.py variable so we can use "flask run" from the shell
    6.1 Also put FLASK_DEBUG=1 and FLASK_ENV=development

7. Create "config.py" file for configuration files
    7.1 Import os
        7.1.1 basedir = os.path.abspath(os.path.dirname(__file__))
    7.2 Create "Config" class
    7.2 Put "SECRET_KEY" as a class variable. Use "OR" constructor with os.environment.get('SECRET_KEY') function

8. Import the "Config" class to __init__.py module
    8.1 set "app.config.from_object(Config)" after the "app" instance

_______

9. Create forms.py module
    9.1 Import FlaskForm from flask_wtf
    9.2 Import String, Boolean, Submit, Password fields from wtforms
    9.3 Import DataRequired from wtforms.validators

10. Create a class LoginForm that inherits from FlaskForm
    10.1 Create username, password, remember_me and submit as class variables
    10.2 Each variable is an object instantiated from wtforms classes (StringField, BooleanField...)
    10.3 Each object should be instantiated with label as first argument and validators=[DataRequired()] as second
        10.3.1 Except remember_me and submit variables. They will have only label names

11. Create "login.html" inside Templates folder
    11.1 It inherits from "base.html"
    11.2 It will have a "<form>" with 4 "<p>"s in it for each of the class variables (username, password...)
        11.2.1 Example of a form:

            {{form.username.label}} <br> <- this is a breakline
            {{form.username(size=32)}}

        11.2.2 remember_me and submit will be called as a function (with brackets):

           {{form.remember_me()}}
           {{form.remember_me.label}}

        11.2.3 submit will not have label form

    11.3 It will also have a {{form.hidden_tag()}} on top of paragraphs right after <form>

    11.4 Form will have <form action="" method="post" novalidate>
        11.4.1 action="" means that all the data submitted will be reflected in url
        11.4.2 The novalidate attribute is used to tell the web browser to not apply validation to the fields in this form, which effectively leaves this task to the Flask application running in the server. Using it is optional, but for this first form it is important that we set it because this will allow us to test server-side validation later.

_______

12. Inside _routes.py_ create a new view function for login
    12.1 Import flash, redirect functions from flask

    12.2 Create if statement after form=LoginForm()
        12.2.1 if form.validate_on_submit() then use flash with a message
        12.2.2 this message will use string formatting with form.username.data and form.remember_me.data
        12.2.3 return redirect('/index')

    12.3 form.validate_on_submit() is a flask function. It does all the processing work. If it receives GET request (just reloading the page for instance) then it is false. If it will get POST request (clicking submit, sign in buttons) then it is true

13. We will need to render the flashed messages (get_flashed_messages() from flask) in browser. So, inside _base.html_
    13.1 After <hr> element create a jinja templates
        13.1.1  {% with %} statement containing messages variable
                {% if %} statement indicating, if messages are true, then
                {% for %} statement looping through each message and...

        13.1.2 Displaying each message as a <li> item inside <ul>

        13.1.3 Close all jinja templates from above

14. We will create an error message in login page, when invalid data or no data is passed. So inside _login.html_
    14.1 Inside <p> after each input field add for loop
        14.1.1 {% for error in form.username.errors%}
    14.2 Add <span> inside the *for loop*
        14.2.1 <span style="color:red">[{{error}}]<span>
        14.2.2 _errors_ are list, because validators (DataRequired()) can have more than one error

15. Import *url_for* function from flask inside _routes.py_
    15.1 Update _login_ view with it, in the _redirect_ function

    15.2 In the _base.html_ update the header <div> with url_for as well.
        15.2.1 Note, that url for will be inside "", like "{{url_for('index')}}"

_______

16. pip3 install flask-sqlalchemy flask-migrate

17. Inside _config.py_
    17.1 basedir = os.path.abspath(os.path.dirname(__file__))
    17.2 create SQLALCHEMY_DATABASE_URI variable with _or_ construction like in SECRET_KEY
        17.2.1 Key name is "DATABASE_URI"
        17.2.1 db used is sqlite - use string formatting with basedir (os.path.join)
    17.3 create SQLALCHEMY_TRACK_MODIFICATIONS = False

18. Inside __init__.py
    18.1 Import SQLalchemy from flask_sqlalchemy
    18.2 Import Migrate from flask_migrate

    18.3 Instantiate "db, migrate" objects from those two classes
        18.3.1 db object will have (app) as an argument
        18.3.2 migrate object will have (app, db) as arguments

    18.4 Import _models_ from app, after _routes_
        18.4.1 So far models.py file is not created

19. Create _models.py_ inside app directory
    19.1 Import db from app

    19.2 Create a **User** class, which inherits from **db.Model**
        19.2.1 Create _id_ object instantiated from db.Column class. Type db.Integer, primary key true.
        19.2.2 Create _username_ object instantiated from db.Column class. Type db.String(64), index true, unique true.
        19.2.3 Create _email_ object instantiated from db.Column class. Type db.String(120), index true, unique true.
        19.2.4 Create _password-hash_ object instantiated from db.Column class. Type db.String(128).

    19.3 Create __repr__ method
        19.3.1 It returns something meaningful (User: Mufasa for instance) when object is called

**WORKING WITH DATABASES**
20. Do _flask db init_
    20.1 It will initialize db and create migrations folder

21. Do _flask db migrate -m "users table"_
    21.1 It will create a migration script (...\002480c47_user_table.cpython-37.pyc) in _versions_ subdirectory
    22.2 This is the initial db migration, which will create **app.db** file inside the project folder

22. Do _git init_
    22.1 Before we _upgrade_ the database, we will create a git repository and push it to github for version control
    22.2 _git add ._ then _git commit -m "useful message"_
    22.3 _git config user.name ""_ then _git config user.email ""_ give the long email from Github
    22.4 Create a new repository on Github and copy SSH url
    22.5 Do _git remote add origin url_ to connect local repo to Github
    22.6 Do _git remote -v_ to check if all is fine
    22.7 Do _git push origin master_

23. Do _flask db upgrade_

**DB MIGRATION**
Flow of database changes:
    1. change the model (add new tables, remove, change the schema and so on)
    2. _flask db migrate -m "comments"_ to create a new migration script
    3. Review the changes to make sure _migrate_ did the right things
    4. _flask db upgrade_ to apply the new changes in the script to development db
    5. git add, commit, push to branch, review the changes then merge
    6. When you are ready to release the new version of the application to your production server, all you need to do is grab the updated version of your application, which will include the new migration script, and run _flask db upgrade_. Alembic will detect that the production database is not updated to the latest revision of the schema, and run all the new migration scripts that were created after the previous release.
    7. We also have a _flask db downgrade_ command, which undoes the last migration. We may have generated a migration script and applied it, only to find that the changes that we made are not exactly what we need. In this case, we can downgrade the database, delete the migration script, and then generate a new one to replace it.
**READ THIS SECTION**

24. Create **Post** class that will inherit from **db.Model**
    24.1 Create _id_ object instantiated from db.Column class. Type db.Integer, primary key true.
    24.2 Create _body_ object instantiated from db.Column class. Type db.String(140).
    24.3 Create _timestamp_ object instantiated from db.Column class. Type db.DateTime, index true, default=datetime.utcnow
    24.4 Create *user_id* object instantiated from db.Column class. Type Integer, db.ForeignKey("user.id")
        24.4.1 Note this "user" is reference to **User** class and its id column. It is unfortunate that db.Model accepts only
               lower case arguments.
    24.5 Create __repr__ function to return the body when asked

    24.6 Inside **User** class add _posts_ object instantiated from _db.relationship_
        24.6.1 Arguments for relationship are _"Post"_ - reference to class, _backref_ - will add a _post.author_ expression that will return the user if given a particular post, _lazy_ - defines how the database query for the relationship will be issued. More info on _lazy_ is here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

25. We will create a migration script for the new table (Post) and upgrade it. Repeat step 21.
    25.1 Do _flask db migrate -m "post table"_
    25.2 Do _flask db upgrade_
    25.3 Push to Github.

26. Inside _microblog.py_ import db. Also, import User, Post from app.models
    26.1 Function will be created using *@app.shell_context_processor* decorator
    26.2 Function is *make_shell_context*
    26.3 It wil return a dictionary {'db':db, 'User':User, 'Post':Post}

    _Note_
    This is done to manage _Flask shell_ command in the terminal. We can use this command to launch flask app as a playground and test if the models we designed are working properly by creating sessions, adding users, posts to tables and returning them.
    **Important!** Do not forget to delete the session and all the added users before exiting shell!
    More info is here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

 _______

 27. Import *generate_password_hash, check_password_hash* from _werkzeug.security_ in **models.py**
    27.1 Inside _Users_ class, create two new methods: *set_password* and *check_password*
    27.2 First method has _self, password_ arguments and creates a variable named `self.password_hash` using the _generate..._ function
        27.2.1 It does not return anything
    27.3 Second method returns *check_password_hash(self.password_hash, password)*

28. Do _pip install flask-login_
    28.1 Inside _init.py_ import **LoginManager** from *flask_login*
    28.2 Right after `app, db, migrate`, create a `login` variable as an instance of _LoginManager_

29. Inside _models.py_ import _UserMixin_ from *flask_login*
    29.1 Add this **UserMixin** as class argument into _User_ class
    29.2 More info on what UserMixin actuall is here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

30. In the _models.py_ import *login* from *app*
    30.1 After User, Post classes, create a function *load_user(id)*
    30.2 This function will have a decorator above it, **@login.user_loader**
    30.3 Function itself will return *User.query.get(int(id))*

31. In the _routes.py_ import **User** from `app.models`, and *current_user, login_user, logout_user* from `flask_login`

32. Change the `login` function
    32.1 If the user is already logged in and tries to go to login page by mistake, redirect them to the main page
        32.1.1 We can accomplish it by using *if current_user.is_authenticated: redirect(url_for('index'))*
    32.2 Inside `form.validate_on_submit()`, do the following:
        32.2.1 Query the user from **User** and save it into variable `user`
        32.2.2 If this user does not exist or his/her password hash does not match (use `user.check_password` function),
                then flash an error message, stating that username or password is incorrect
                *AND* redirect the session back to the _login_ page
        32.2.3 Else (if user exists and password is correct), then `login_user(username=user, remember=form.remember_me.data)`
        32.2.4 Redirect to the main page

33. Add `logout` function
    33.1 Log the user out and redirect to the main page
    33.2 Do not forget the _app.route("/logout")_ decorator

34. Inside the _base.html_, in the `header of the page`
    34.1 Add *if statements* using jinja templates
    34.2 If current user is anonymous, then he/she will see `Login` url
    34.3 If not, he/she will see `Logout` url

 _______

35. Inside __init.py__ create after _login = LoginManager(app)_
    35.1 create `login.login_view = 'login'`
    35.1 The 'login' value above is the function (or endpoint) name for the login view.
         In other words, the name we would use in a `url_for()` call to get the URL.

36. Inside `login` view, after *login_user* is done
    36.1 Obtain the `next_page` variable from `request.args.get('next')`
    36.2 You need to import _request_ from **flask** and *url_parse* from **werkzeug.urls**
    36.3 Create and _if_ statement after
        36.3.1 Check if *next_page*or its *netloc* component is not empty: `not next_page or url_parse(next_page).netloc != ""`
        36.3.2 If any one of them is true, set the url for variable *next_page* to `index` view
        36.3.3 Otherwise, it will remain the url you got before from `reqeust.args.get('next')`
        36.3.4 More on **netloc** is here: https://stackoverflow.com/questions/53992694/what-does-netloc-mean

37. Protect your `index` view with **login_required** decorator after _@app.route_
    37.1 You need to import *login_required* from **flask_login**

38. Now, as login functionality is created, inside _index.html_
    38.1 change the `user` to `current_user` in <h1> tag, as we can utilize flask_login functionality

39. Inside _routes.py_ remove `user=user` from *render_template* of `index` view
    39.1 We do not need to provide a user anymore

_______

40. Inside **forms.py** create `RegistrationForm` _class_
    40.1 add _ValidationError, Email, EqualTo_ to *wtforms.validators* import
    40.2 from _app.models_ import `User`
    40.3 Create the class
        40.3.1 It will have five fields `username, email, password, password2, submit`
            40.3.1.1 Each will use `fields` from _wtforms_ and have appropriate _validators_
            40.3.1.2 You can check the **LoginForm** class for details, as they are similar
            40.3.1.3 `password2` is to make sure the user typed the password twice, hence *EqualTo* is used

    40.4 This class will have two additional _custom validators_
        40.4.1 `validate_username(self, username)`, which will check if the user already exists
                and if so, will raise and exception using *ValidationError*
        40.4.2 `validate_email(self, email)`, which will check if the email is unique, and if not,
                it will raise a similar error
        40.4.3 Query the User table with *filter_by(username=username.data).first()* and save to `user` variable
        40.4.4 Same for email

41. Create *register.html* inside __templates__ folder
    41.1 Put a form for `Registration` similar to _login.html_
    41.2 It will extend the `base.html` and be practically the same
    41.3 After the login form, create a <p> with inviting new users to registration

42. Inside _routes.py_ create a view for `Registration` with `register` function
    42.1 Import *RegistrationForm* and add after *LoginForm* in the imports
    42.2 from _app.models_ import **User**, which will be queried inside the `register` view
    42.3 The `register` function itself will be almost identical to `login` view, with minor differences
        42.3.1 It will use *user.set_password(form.password.data)*
        42.3.2 It will have `db.session.add` and `db.session.commit` to upload the user to db

_______

43. Inside _routes.py_ create a new view function, `user(username)` which will be his/her **Profile page**
    43.1 `login_required` is needed
    43.2 This function will have dynamic url, which is that `<username>` in the string
        43.2.1 We can pass it as a query argument to retrieve the user
        43.2.2 *first_or_404()* is a method which gives 404 error if there is no user with that username
    43.3 It will also have list of fake posts
        43.3.1 `"author":user, "body":"test post #1"`
    43.4 We will render a new template with user and posts

44. Create a new _user.html_ file which extends _base.html_
    44.1 Very simple header1 with the username
    44.2 Loop through the posts and show them

45. Inside _base.html_ add a link to **Profile**
    45.1 We will write it inside the `else` clause, because it should be shown only if the user is logged in
    45.2 Because Profile will appear only for logged in users, we can use `current_user.username` inside *url_for*
        45.2.1 `url_for('user', username=current_user.username)`

________

46. **Gravatar**. Inside the _models.py_ add `avatar(email)` function to **User** class
    46.1 It will transform the user's email to `md5 hash`
        46.1.1 `digest = md5(self.email.lower().encode("utf-8")).hexdigest()`
    46.2 We will return an Gravatar link with the hash and identicon, in case email does not exist in Gravatar
        46.2.1 `f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"`

47. Inside _user.html_ change the header
    47.1 Wrap the header within a <table>, which has <tr valign="top"> consisting of <td>s
        47.1.1 <td> <img src="{{user.avatar(size=128)}}" alt="Gravatar image"> </td>
    47.2 To add the gravatar to individual posts, you also wrap the posts inside <table>, <tr valign="top">, <td> without <p>

48. We create *_posts.html*, which is a sub-template and put our post in it as a table from the step 47
    48.1 We will reference it in the *user.html* using the `{% include "_posts.html" %}` clause
    48.2 The _ prefix is just a naming convention to help us recognize which template files are sub-templates.
________

49. Inside the **User** class, we add two columns
    49.1 `about_me` so users can add descriptions to their profile. It is just a _db.String(140)_
    49.2 `last_seen`, to show when the user was on the site last time
        49.2.1 `db.Column(db.DateTime, default=datetime.utcnow)`

50. Every time the database is modified it is necessary to generate a database migration.
    50.1 We do _flask db migrate -m "comment"_ to migrate
    50.2 Then _flask db upgrade_ to apply the changes to our `app.db`
    50.3 Any users that were in the database are still there, the migration framework surgically applies the changes in the migration script without destroying any data.

51. In the _user.html_ we add two conditionals for `about_me` and `last_seen` views
    51.1 Because we only want them to be visible if they are set. 
        51.1.1 `{% if user.about_me %} <p>{{user.about_me}}</p> {% endif %}`
    51.2 At this point these two new fields are empty for all users

________

52. In the _routes.py_ file, we add a new `before_request` function
    52.1 We use this function to set `last_seen` of our *current_user* to `datetime.utcnow()`
        52.1.1 We check if the user is authenticated, if so, set the last_seen, then `db.session.commit()`
    52.2 It will have an `@app.before_request` decorator
    52.2 This decorator from Flask registers the decorated function to be executed right before the view function.
         This is extremely useful because now we can insert code that I want to execute before any view function in the application, and we can have it in a single place.
    52.3 Why there is no `db.session.add()` before the commit, consider that when you reference current_user, Flask-Login 
         will invoke the user loader callback function, which will run a database query that will put the target user in the database session. So you can add the user again in this function, but it is not necessary because it is already there.

    52.4 **So in a nutshell, this function is used to do something right before html pages are loaded or view functions are ran**
________

53. Create *edit_profile.html* file
    53.1 It will show the `EditProfileForm` from _forms.py_ which you should create. More on the next point

54. In the _routes.py_ we create a new view function `edit_profile`
    54.1 It will use the `EditProfileForm` class from _forms.py_
        54.1.1 This class has three fields to be shown on the webpage, _username, about-me, submit_
    54.2 If validate_on_submit() returns **True** I copy the data from the form into the user object and then write the  
         object to the database.
    54.3 In case it is **False**, it might be either because we get an initial `GET` request 
         when the page is loaded for the first time, or `POST` but with some validation error
         54.3.1 In case of initial `GET`, we need a reverse operation, **set the form data from current_user data**, 
                instead of setting the current_user from the form data. 
                Because in the initial load, there will not be anything submitted by the user.
                We check it by `request.method == "GET" `
         54.3.2 In case we receive `POST` but with some validation errors, we do not want to write anything to the form 
                fields, because those were already populated by WTForms.
                That is why we do not have `else` clause - we just skip the `POST` with validation errors
    54.3 We add a link to _Edit profile_ in the _user.html_ template
        54.3.1 Inside the <table> <tr> <td> after <h1>
        54.3.1 Pay attention to the clever conditional (if user == current_user) to make sure that the Edit link appears when you are viewing 
               your own profile, but not when you are viewing the profile of someone else
    54.4 **Always check your database if you have all the columns properly populated with data**
________

**Bug: Duplicate username change in the edit profile**
55. Create _errors.py_ in the app directory
    55.1 Import *render_template* from flask, and *app, db* from app
    55.2 Creat two functions `not_found_error(404)` and `internal_error(500)` with *@app.errorhandler(404 or 500)* as decorator
    55.3 They return respective templates `404.html` and `500.html` which are to be created in *templates*
    55.4 Extend _base.html_, content is <h1> for error message, <p><a href='url for index'>Back</a></p>
    55.5 In the **__init__.py** import _errors_ after routes and models
    55.6 Set the FLASK_DEBUG = 0 to test it
________

**Email configurations**
56. In the _config.py_, create the following variables
    56.1 `MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, ADMINS`
    56.2 Values for these variables come from `.flaskenv` with the same names
        56.2.1 Except for `admins`, which is the adress where we want to receive the emails
    56.3 We set the env variables for each of those variables in _.flaskenv_
        56.3.1 `stmp.rambler.ru`, `467`, `True`, `tsueid@rambler.ru`, `password`

57. In the *__init__.py* import `logging` and _SMTPHandler_ from `logging.handlers`
    57.1 If app is not in a debug mode, 
    57.2 If we have the mail server set (which we did)
    57.3 We set the auth to None, but it might change
    57.4 We check if we set username and password, which we did
    57.5 So instead of None, we give username and password to auth
    57.6 So far secure=None
    57.7 However, if we are forcing the handler to user TLS, which we are
    57.8 Set the security to empty tuple to use TLS without certificate or key
    57.9 Create *mail_handler* variable as `SMTPHandler` instance
    57.10 Give it all the named variables it requires
        57.10.1 _fromaddr_ should be the same email address (_tsueid@rambler.ru_)
    57.11 We only want the logs that are errors, not debug or warnings - *mail_handler.setlevel(logging.ERROR)*
    57.12 Pass the *mail_handler* to app logger - `app.logger.addHandler(mail_handler)`
________

**Error logging**
58. In the *__init__.py* add _RotatingFileHandler_ to the import of `logging.handlers`
    58.1 Import `os` too

59. Inside the `if` clause (`if not app.debug`), after *mail_handler* is added to `app.logger.addHandler`
    59.1 If the path `logs` does not exist, create a directory `logs`
    59.2 Create *file_handler* variable, which is an instance from `RotatingFileHandler`
        59.2.1 It will have three arguments: `"logs/microblog.log", maxBytes=10240, backupCount=10`
    59.3 Set the formatter on the file_handler
        59.3.1 `logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")`
    59.4 Set the file_handler level to _logging.INFO_
    59.5 add the *file_handler* to the logger: `app.logger.addHandler(file_handler)`
    59.6 Set the logging level to INFO on app level too `app.logger.setLevel(logging.INFO)`
    59.7 `app.logger.info("Microblog startup")`
________

**Fixing the duplicate username bug**
60. In the _forms.py_, `EditProfileForm` class, create an `__init__` method
    60.1 It will accept `self, original_username, *args **kwargs`
    60.2 We will pass the _*args, **kwargs_ to its parent class
        60.2.1 `super(EditProfileForm, self).__init__(*args, **kwargs)`
        60.2.2 create an instance variable with original username: `self.original_username = original_username`
    60.3 Create *validate_username(self, username)* method
        60.3.1 we check if the new entered name is not equal to what we have in db
        60.3.2 if so, we check if the new entered name exist in db by querying the User
        60.3.3 if new chosen name is the same as in our db, we raise an error
            60.3.3.1 `raise ValidationError('Please use a different username.')` 

61. In the _routes.py_ modify the `edit_profile` form
    61.1 `form = EditProfileForm(current_user.username)`, because of that `__init__` method of `EditProfileForm` class
________

**FOLLOWERS** - [Link](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers)
> We have to create _many-to-many_ relationship between follower users and followed user.
> Because both users live in the `User` table, we will have to self connect it to itself.
> A relationship in which instances of a class are linked to other instances of the same class 
> is called a _self-referential relationship_, which we will implement using an association table.

62. In the _models.py_ create a `db.Table` named _followers_, which is an **association table** for **many-to-many**
    62.1 It will have three arguments: name of the table (`followers`), and two columns
    62.2 Two columns are:
            `db.Column("follower_id, db.Integer, db.ForeignKey(user.id))`
            `db.Column("followed_id, db.Integer, db.ForeignKey(user.id))`

63. Inside the `User` class, create a `db.relationship` named _followed_
    63.1 `'User'` is the right side entity of the relationship (the left side entity is the parent class). 
        Since this is a self-referential relationship, we have to use the same class on both sides.
    63.2 `secondary=followers` configures the association table (step 62) that is used for this relationship.
    63.3 `primaryjoin=(followers.c.follower_id == id)` links the left side (the follower user) with the association table. 
        63.3.1 *followers.c.follower_id* references the *follower_id* column of the association table.
        63.3.2 `c` is an attribute of SQLAlchemy tables not defined as models. For them, columns are exposed as sub-attributes of "c".
    63.4 `secondaryjoin=(followers.c.followed_id == id)` links the **right** side (the followed user) with the association table. 
    63.5 `backref=db.backref('followers', lazy='dynamic')` defines how this relationship will be accessed from the right side entity. 
        From the left side, the relationship is named followed, so from the right side we use the name followers to represent all the left side users that are linked to the target user in the right side. The additional *lazy* argument indicates the execution mode for this query. A mode of *dynamic* sets up the _query to not run until specifically requested_.
    63.5 `lazy='dynamic'` is similar to the parameter in the backref, but this one applies to the left side query instead of the right side.

64. Do `flask db migrate -m "followers association table"`
    64.1 Do `flask db upgrade`
    64.2 Push to git
    
65. Thanks to the SQLAlchemy, a user following other user can be recorded in the db working with the _followed_ relationship as a list.
    65.1 So, we do `user1.followed.append(user2)`, which will put the _user1_ in `follower_id` and _user2_ in `followed_id` columns
    65.2 Same works for `user1.followed.remove(user2)`

66. In the `User` class, add three methods
    66.1 _follow_, which has `self` and `user` arguments, it checks if *self* is _not already following_ (`is_following` method) the *user*
        66.1.1 If so, `self.followed.append(user)`
    66.2 _unfollow_, which accepts `self` and `user` argument, it check if *self* is _already following_ the *user* (`is_following`)
        66.2.1 If so, `self.followed.remove(user)`
    66.3 *is_following* a helper method to check if `self` is already following the `user`
        66.3 It returns `True` or `False`
        66.4 To achieve it we will query the _followed_ table from the point of _self_ - `self.followed.filter()`
            66.4.1 _filter_ condition is `followers.c.followed_id == user.id`: take the followed_id from followers table
            66.4.2 and check if any of them equal to user.id
        66.5 This query can return either 0 or 1, because either self will have a counterpart (in the next column) user.id or not
        66.6 So, the whole clause is `return self.followed.filter(followers.c.followed_id == user.id).count() > 0`

67. We need a query to obtain all the posts from followed users, AND our own posts
    67.1 _SQL query_ is as follows
        ```
        SELECT 
            post.user_id,
            post.body
        FROM post JOIN followers
        ON post.user_id = followers.followed_id
        WHERE followers.follower_id = 1
        UNION
        SELECT
            post.user_id,
            post.body
        FROM post
        WHERE post.user_id = 1
        ORDER BY post.timestamp DESC;
        ```
    67.2 Corresponding _Python code_ added in the `User` class is such
        ```
        def followed_posts(self):
            followed_ones = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
            own_posts = Post.query.filter_by(user_id=self.id)
            return followed_ones.union(own_posts).order_by(Post.timestamp.desc())
        ```
________

**UNIT TESTING THE USER MODEL**
68. Create _tests.py_ in the main directory
*Tests are self explanatory. No need to write down what they do*
    68.1 from datetime import datetime, timedelta
    68.2 import unittest
    68.3 from app import app, db
    68.4 from app.models import User, Post

**FOLLOW, UNFOLLOW FUNCTIONALITY**
69. Inside _forms.py_ create a form (`EmptyForm(FlaskForm)`)
    69.1 which will have just one `submit` button

70. Inside _routes.py_ create two routes
    70.1 one for following (`app.route('/follow/<username>')`)
    70.2 one for unfollowing (`app.route('/unfollow/<username>')`)
    70.3 both will have `methods=["POST"]`
    70.4 both will have `@login_required`
    70.5 both functions will accept _username_ as an argument

71. Create an instance of the _EmptyForm_
        70.1 if it passes the validations, query the _User_ by the _username_ and save in `user` variable
            70.1.1 check if the `user` is None, flash a message if yes and redirect to _index_
            70.1.2 if it is not None, check if `user==current_user` 
                70.1.2.1 flash a message is yes and redirect to _user_ route (page)
            70.1.3 If both conditions are passes, add the `user` to *current_user's* followers
                70.1.3.1 `current_user.follow(user)`
                70.1.3.2 `db.commit.session()` - save the changes to the database
                70.1.3.3 flash a message and redirect to _user_ route (page)
        70.2 if it does not pass the validations, redirect to _index_
        70.3 **unfollow route will be identical**

72. To add this submit button to the _user_ route (page)
    72.1 inside the _user_ route, instantiate _EmptyForm_
        72.1.1 `form = EmptyForm()`
    72.2 and pass the form into the `render_template` functions
        72.2.1 `return render_template("user.html", user=user, posts=posts, form=form)`

73. Inside the _user.html_
    73.1 add <p> paragraph after the `Last seen on:`
        73.1.1 show how many followers the user has and how many he/she is following
        73.1.2 `{{user.followers.count()}}` to access the followers' count
        73.1.3 `{{user.followed.count() }}` to access the followed count
    73.2 add two more conditionals to dynamically change the link on top the page
        73.2.1 if the `user=current_user` then the link is _Edit Profile_, we already have it in the step 53
        73.2.2 elif `not current_user.is_following(user)` then create a paragraph
            73.2.1.1 this paragraph will have a form with hidden tag and submit button from _EmptyForm_
            73.2.1.2 form action is `action="{{ url_for('follow', username=user.username) }}"` and `method="POST"`
            73.2.1.2 `form.submit(value="Follow")` after the hidden tag
        73.2.3 else, then create another paragraph, identical to the previous
            73.2.3.1 but `form.submit(value="Unfollow")` after the hidden tag
________

**TEXTING AREA TO THE MAIN PAGE**
74. Inside _forms.py_
    74.1 create `class PostForm(FlaskForm)`
        74.1.1 it will have `post` variable with _TextFieldArea_
            74.1.1.1 data validators are _DataRequired()_ and _Length(min=1, max=140)_
        74.1.2 and `submit` variable with _SubmitField('Submit')_

75. Pass the _PostForm_ to the `index` route inside _routes.py_
    75.1 import the form on top (and Post class alongside User class)
    75.2 add `methods=['GET', 'POST']` to the _app.route()_ decorators
    75.3 instantiate a form
    75.4 `if form.validate_on_submit()`
        75.4.1 create `post = Post(body=form.post.data, author=current_user)`
        75.4.2 add the _post_ to the db
        75.4.3 commit the session
        75.4.4 flash a message
        75.4.5 redirect to the `index` route
            75.5.5.1 **This is called POST/redirect/GET pattern**
        75.4.6 replace the _posts_ variable which had fake posts before
            75.4.6.1 with `posts = current_user.followed_posts().all()`
    75.5 add the _form_ to the *render_template*

76. Inside the _index.html_
    76.1 add a <form> after the <h1> tag
    76.1 which will have a hidden_tag as usual
    76.2 and uses the _form_ from the `index` route
        76.2.1 by having two fields (text area and submit) inside <p> tags
        76.2.2 do not forget to display the errors (as <span>) after text area inside jinja for loop

77. Inside _routes.py_
    77.1 create an `explore` route
    77.2 login is required
    77.3 query all the posts (order by timestamp) into a variable
        77.3.1 `posts = Post.query.order_by(Post.timestamp.desc()).all()`
    77.4 `render_template('index.html', title='Explore', posts=posts)`
        77.4.1 **pay attention that we are reusing the _index.html_ when rendering**
        77.4.2 because explore page will be similar to the main page

78. Inside _base.html_
    78.1 add <a> ref to the `explore` page after the _Main Page_
        78.1.1 use `url_for('user', username=post.author.username)` as _href_

79. Inside *_posts.html*
    79.1 change the {{user.avatar(36)}} to {{post.author.avatar(36)}}
    79.2 wrap the {{post.author.username}} in the second <td> with <a> tag
        79.2.1 _href_ is `url_for('user', username=post.author.username)`

80. Inside the _index.html_
    80.1 wrap the form the step 76 with a jinja if
        80.1.1 `{% if form %} form from step 76 {% endif %}`
    80.2 **this allows us to reuse the _index.html_ in both Main Page and in Explore page**
        80.2.1 this if condition allows us to skip the _form_ in the *Explore* page

81. In the same file, change the for loop for posts
    81.1 Instead of the <div> with <p> tags
    81.2 just do `{% include '_posts.html' %}`
    81.3 **both Main page and Explore pages now use the same html file**
________

**PAGINATION**
82. Inside _config.py_ set `POSTS_PER_PAGE=3` which later will be changed to `25`

83. Inside _routes.py_ file, modify the `index` and `explore` routes
    83.1 add `page` variable to both, which is equal to `requests.args.get('page', 1, type=int)`
        83.1.1 it means that from the _url_ in search bar, get the `page` query parameter
        83.1.2 if it does not exist, then the default is `1`
    83.2 change the `posts` variable in both functions
        83.2.1 instead of `.all()` use `.paginate(page, app.config['POSTS_PER_PAGE'], False)`
            83.2.1.1 `page` argument is our variable from the previous step
        83.2.2 `.paginate(start, end, error_flag)` is offered by Flask
            83.2.2.1 if *error_flag* is set to _True_, it returns `404` if the current number is out of range
            83.2.2.2 if it is set to _False_ (which we did), it returns an empty list in case of out of range
    83.3 set the _posts_ in the *render_tempate* to `posts.items`
        83.3.1 because previous _paginate_ function returns a _Paginate_ object
        83.3.2 which offers `items` attribute, which in our case is a list of posts from db

84. This _Paginate_ object also has another _4 attributes_
    84.1 
        ```
            has_next: True if there is at least one more page after the current one
            has_prev: True if there is at least one more page before the current one
            next_num: page number for the next page
            prev_num: page number for the previous page
        ```        

85. Inside the _routes.py_ modify `index` and `explore` routes
    85.1 add `next_url` and `prev_url` variables to both of them
        85.1.1 we use *ternary conditional* for it
    85.2 they are set to 
        `url_for('index', page=posts.next_num) if posts.has_next else None`
        `url_for('index', page=posts.prev_num) if posts.has_prev else None`
        for _index_ route
    85.3 and 
        `url_for('explore', page=posts.next_num) if posts.has_next else None`
        `url_for('explore', page=posts.prev_num) if posts.has_prev else None`
        for _explore_ route
    85.4 pass both variables to the *render_template* function

86. In he _index.html_ add jinja if statements for `prev_url` and `next_url` variables
    86.1
        ```
            {% if prev_url %}
                <a href="{{ prev_url }}">
                    Newer posts
                </a>    
            {% endif %}
        ```
        for new posts
    86.2
        ```
            {% if next_url %}
                <a href="{{ next_url }}">
                    Older posts
                </a>    
            {% endif %}
        ```
        for older posts

87. Inside the _routes.py_ modify the `user` routes, delete the fake data
    87.1 add `page`, `posts`, `next_url`, `prev_url` variables similar to previous steps
        87.1.1 `url_for` for the next and prev urls should have an extra `username=user.username` argument
        87.1.2 it is to make sure that we are redirecting the click to the same page (user's page)
    87.2 `posts` variable is queried from the existing `user` variable
        87.2.1 `posts=user.posts.order_by(...).paginate(...)`
        87.2.2 _User_ model has _posts_ attribute which is a _db.relationship_
            87.2.2.1 SQLAlchemy already set it up as a query, so we can immediately use `order_by` on it
            87.2.2.2 alternative would be query the _Post_ model with _author_ backref being the `user`
    87.3 pass all the new variables to *render_template* functions
        87.3.1 do not forget `posts` is now a _Pagination_ object

88. Inside the _user.html_ add jinja if statements for *next_url* and *prev_url*
    88.1 They are the same from the _index.html_

89. Inside _config.py_
    89.1 change the `POSTS_PER_PAGE` to `25`
________

**SENDING EMAILS FOR PASSWORD RESET**

90. Install flask-mail, pyjwt packages from pip
    90.1 import Mail from flask_mail in the *__init.py__* file
    90.2 initiate Mail instance there as `mail = Mail(app)`

91. In the _app_ folder, create a _email.py_ file
    91.1 from flask_mail import Message
    92.2 from _app_ import `mail`
    92.3 create `send_email(subject, sender, recipients, text_body, html_body)` function
        92.3.1 msg = Message(subject=subject, sender=sender, recipients=recipients)
        92.3.2 msg.text = text_body
        92.3.3 msg.body = html_body
        92.3.4 mail.send(msg)
    92.4 create `send_password_reset_email(user)` function after
        92.4.1 _pass_ so far

92. In the _login.html_ add another <p>
    92.1 
    ```
        <p>
            Forgot password?
            <a href="{{ url_for('reset_password_request') }}">
                Click to reset it!
            </a>
        </p>
    ```

93. In the _forms.py_ add `RequestPasswordResetForm` class
    93.1 it will have `email` as StringField with the related validators
    93.2 and `submit` button as a SubmitField

94. In the _routes.py_ create another route for password reset
    Import the class from 93th step, and *from app.email import send_password_reset_email*
    94.1 `@app.route("/reset_password_request", methods=["GET", "POST"])`
    94.2 if the current user is authentcated then redirect to index
    94.3 query the User by email
    94.4 if `user` exist then `send_password_reset_email(user)`
    94.5 flash a message that instructions were sent
    94.6 redirect to login page
    94.7 render *reset_password_request.html* with title and form

95. In the _templates_ create *reset_password_request.html*
    95.1 extends base
    95.2 inside the block is <h1> and <form> with post method, no action
        95.2.1 don't forget the hidden tag
        95.2.2 two <p>s: one for email and one for submit button
        95.2.3 jinja for for errors (inside span) in the email paragraph
    *Similar to login or register forms*

96. In the _models.py_ import app from app, import time from time and import jwt
    96.1 create two methods in the `User` class `get_reset_password(self, expires_in=600)` and `verify_reset_password(token)`
    96.2 the first one returns `jwt.encode()`
        96.2.1 payload is `{'reset_password':self.id, 'exp':time() + expires_in}`
        96.2.2 secret key is loaded from `app.config`
        96.2.3 algorithm is 'HS256'
    96.3 the latter is _@staticmethod_ and returns `User.query.get(id)`
        96.3.1 `id` is set in a _try...except_ block
        96.3.1 try `jwt.decode(token, secret-key from app.config, algorithms=['HS256'])['reset_password]`
        96.3.2 expect is just a return nothing

97. Inside the _template_ folder create _email_ folder
    97.1 add `reset_password.txt` and `reset_password.html` files there
    97.2 they will use _jinja_ templates for user and generated url
        97.2.1 generated url will point towards `reset_password` route, which are created in the step 100
    97.3 otherwise, they are fairly simple
    97.4 __When _external=True is passed as an argument, complete URLs are generated__

98. Inside the _email.py_ file finish the `send_password_reset_email(user)` function
    98.1 create a token variable which is set to `user.get_reset_password`
    98.2 then use the `send_mail` generic function
        98.2.1 give a subject
        98.2.2 sender is `ADMINS` from the _app.config_
        98.2.3 recipient is _user.email_
        98.2.4 text_body is `render_template('email/reset_password.txt', user=user, token=token)`
        98.2.5 html_body is `render_template('email/reset_password.html', user=user, token=token)`
            98.2.5.1 __that is why we used jinja inside both txt and html files__

99. Inside the _forms.py_ create `ResetPasswordForm` class
    99.1 it will have three fields `password`, `confirm_password` and `submit`
    99.2 don't forget the validators, especially `EqualTo()` for the second field

100. Inside the _routes.py_ import the `ResetPasswordForm`
    100.1 create `reset_password` route with GET, POST methods
    100.2 function will accept `token` and query parameter is `reset_password/<token>`
    100.3 if the current user is authenticated then redirect to index
    100.4 `user = User.verify_reset_password(token)` static method to check
    100.5 if user is nothing then redirect to index
    100.6 instantiate the form from 99
    100.7 if validate on submit is true
        100.7.1 then `user.set_password(form.password.data)`
        100.7.2 then `db.session.commit()`
        100.7.3 then flash a message
        100.7.4 then redirect to login
    100.8 function returns a `render_template('reset_password.html' form=form)` from step 101

101. Inside the _template_ folder create `reset_password.html`
    __It is different from the html with the same name inside the EMAIL folder__
    101.1 extends _base.html_
    101.2 content is <h1>
    101.3 then a form with POST method
    101.4 _don't forget the hidden tag_
    101.5 three <p> paragraphs
    101.6 for each field from the `ResetPasswordForm` and their labels, password size is 32
    101.7 jinja for loop for password field errors and errors are in <span>

**CHANGE THE MAIL_PORT TO 587 IN ORDER TO FLASK_MAIL TO WORK**

102. In the _email.py_ create `send_async_email(app, msg)` function
    102.1   ```
            with app.context():
                mail.send(msg)
            ```
    102.2 `from threading import Thread`
    102.3 instead of `mail.send(msg)` in the *send_email* generic function
        102.3.1 it uses Thread `Thread(target=send_async_email, args=(app, msg)).start()`

**FACELIFT WITH FLASK-BOOTSTRAP**

103. Do `pip install flask-bootstrap`
    103.1 in the *_init_.py* `from flask_bootstrap import Bootstrap`
    103.2 `bootstrap = Bootstrap(app)`
    _WE WILL HAVE TO COPY THE CODE FROM GITHUB AS IT IS LENGHTY TO EXPLAIN EACH CHANGE_
    103.4 replace all the `.html` files with their bootstrap alternatives from github repo
          Repo: https://github.com/miguelgrinberg/microblog/tree/v0.11

**DATES AND TIMES**

104. Do `pip install flask-moment`
    104.1 inside the _init.py_ import `Moment from flask_moment`
    104.2 instantiate an object from it, `moment = Moment(app)`

105. All the templates must include `moment.js` library as a <script>
    105.1 one way to achieve it to inlude the script in the _base.html_, as everything inherits from it

106. In the _base.html_ include a `{% block scripts %} ... {% endblock %}` at the end
    106.1 this is another block exported from _flask-bootstrap_ package, where JavaScript imports are to be included
    106.2 This block is different from other ones in that it comes with some content predefined in the `bootstrap/base.html` template. 
        All I want to do is add the _moment.js_ library, without losing the `bootstrap/base.html` contents. 
        And this is achieved with the `super()` statement, which preserves the content from the `bootstrap/base.html` template. If you define a block in your template without using `super()`, then any content defined for this block in the `bootstrap/base.html ` template will be lost.
    106.3 add `{{ moment.include_moment() }}` after `{{ super() }}` in the block to include the JS library

107. In the _user.html_
    107.1 replace the `{{ user.last_seen }}` with `{{ moment(user.last_seen).format('LLL') }}`
    107.2 it will format the UTC data from the db into `Month DD, YYYY H:MM PM` format

108. In the *_post.html*
    108.1 change the `says:` to `says {{ moment(post.timestamp).fromNow() }}:`
    108.2 it takes the post timestamp in UTC format and converts it into timestamp relative to current time
        108.2.1 such as `7 hours ago` or `2 days ago`
