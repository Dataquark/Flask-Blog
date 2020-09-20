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

**IMPORTANT**
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
