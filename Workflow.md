1. Create a directory
2. Make a virtual environment
3. Install libraries (flask, python-dotenv, flask-wft...)
-------------------------------------------------------------------
4. Create "App" folder
    4.1 Create __init__.py inside "App" folder
        4.1.1 Import, instantiate Flask object (__name__ inside of it), import routes from app
    4.2 Create routes.py inside "App" folder
        4.2.1 Import app from App
        4.2.2 define @app.route and subsequent functions
    4.3 Create "Templates" folder inside
        4.3.1 Create "index.html" and "base.html"
        4.3.2 Index (and any further html files) will inherit from the Base using Jinja templates using {% block content %}{% endblock%}
-------------------------------------------------------------------
5. Create "microblog.py" (top level app) on the top level directory
    5.1 Import the app inside

6. Create ".flaskenv" file and put FLASK_APP=microblog.py variable so we can use "flask run" from the shell
    6.1 Also put FLASK_DEBUG=1 and FLASK_ENV=development

7. Create "config.py" file for configuration files
    7.1 Import os
    7.2 Create "Config" class
    7.2 Put "SECRET_KEY" as a class variable. Use "OR" constructor with os.environment.get('SECRET_KEY') function
8. Import the "Config" class to __init__.py module
    8.1 "set app.config.from_object(Config)" after the "app" instance

-------------------------------------------------------------------
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
        
           {{form.remember_me()}}                                                                                    {                         {{form.remember_me.label}}

        11.2.3 sumbit will not have label form

    11.3 It will also have a {{form.hidden_tag()}} on top of paragraphs right after <form>

    11.4 Form will have <form action="" method="post" novalidate>
        11.4.1 action="" means that all the data submitted will be reflected in url
        11.4.2 The novalidate attribute is used to tell the web browser to not apply validation to the fields in this form, which effectively leaves this task to the Flask application running in the server. Using it is optional, but for this first form it is important that we set it because this will allow us to test server-side validation later.
-------------------------------------------------------------------
12. Inside _routes.py_
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
-------------------------------------------------------------------
16. pip3 install flask-sqlalchemy flask-migrate

17. Inside _config.py_
    17.1 basedir = os.path.abspath(os.path.dirname(__file__))
    17.2 create SQLALCHEMY_DATABASE_URI variable with _or_ construction like in SECRET_KEY
    17.3 create SQLALCHEMY_TRACK_MODIFICATIONS = False

18. Inside __init__.py
    18.1 Import SQLalchemy from flask_sqlalchemy
    18.2 Import Migrate from flask_migrate

    18.3 Instantiate db, migrate objects from those two classes
        18.3.1 db object will have (app) as an argument
        18.3.2 migrate object will have (app, db) as arguments

    18.4 Import _models_ from app, after _routes_
        18.4.1 So far models.py file is not created

19. Create _models.py_ inside app directory
    19.1 Import db from app

    19.2 Create a **User** class, which inherits from **db.Model**
        19.2.1 Create _id_ object instantiated from db.Column class. Type Integer, primary key true.
        19.2.2 Create _username_ object instantiated from db.Column class. Type String(64), index true, unique true.
        19.2.3 Create _email_ object instantiated from db.Column class. Type String(120), index true, unique true.
        19.2.4 Create _password-hash_ object instantiated from db.Column class. Type String(128).

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
    24.1 Create _id_ object instantiated from db.Column class. Type Integer, primary key true.
    24.2 Create _body_ object instantiated from db.Column class. Type String(140).
    24.3 Create _timestamp_ object instantiated from db.Column class. Type DateTime, index true, default=datetime.utcnow
    24.4 Create _user_id_ object instantiated from db.Column class. Type Integer, db.ForeignKey("user.id")
        24.4.1 Note this "user" is reference to **User** class and its id column. It is unfortunate that db.Model accepts only
               lower case arguments.
    24.5 Create __repr__ function to return the body when asked

    24.6 Inside **User** class add _posts_ object instantiated from _db.relationship_
        24.6.1 Arguments for relationship are _"Post"_ - reference to class, _backref_ - will add a _post.author_ expression that will return the user if given a particular post, _lazy_ - defines how the database query for the relationship will be issued. More info on _lazy_ is here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

25. We will create a migration script for the new table (Post) and upgrade it. Repeat step 21.
    25.1 Do _flask db migrate -m "post table"_
    25.2 Do _flask db upgrade_
    25.3 Push to Github.