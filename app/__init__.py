from logging import log
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object(Config)

# environment variables are in config.py
# This is step 18 in the Workflow.md
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# This is step 28 in the Workflow.md
login = LoginManager(app)
login.login_view = "login"  # Step 35 in the Workflow

# models are added in step 18.4 of Workflow.md
from app import routes, models, errors

# Step 57 in the workflow
# If app is not in a debug mode
if not app.debug:
    # if we have the mail server set (which we did)
    if app.config["MAIL_SERVER"]:
        # we set the authorisation to nothing, but it might change
        auth = None
        # we check if we set username and password, which we did
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            # so instead of None, we give username and password to authorisation
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        # so far security is nothing
        secure = None
        # however, if we are forcing the handler to user TLS, which we are
        if app.config["MAIL_USE_TLS"]:
            # set the security to empty tuple to use TLS without certificate or key
            # in production level, we should give cerificate and key
            secure = ()

        # mail handler that will be passed to app.logger.addHandler
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="tsueid@rambler.ru",
            toaddrs=app.config["ADMINS"],
            subject="Microblog failure",
            credentials=auth,
            secure=secure,
        )
        # we only want the logs that are errors, not debug or warnings
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
