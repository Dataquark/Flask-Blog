from logging import log
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)

# environment variables are in config.py
# This is step 18 in the Workflow.md
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# This is step 28 in the Workflow.md
login = LoginManager(app)
login.login_view = "login"  # Step 35 in the Workflow

# step 90 in the Workflow
mail = Mail(app)

# step 103 in the workflow
bootstrap = Bootstrap(app)

# step 104 in the workflow
moment = Moment(app)

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

    # if the path logs does not exist
    if not os.path.exists("logs"):
        # create a directory, otherwise move on
        os.mkdir("logs")
    # loggins files handler that will be passed to app.logger.addHandler
    # Giving max size of the file, and keeping max 10 files in the directory
    file_handler = RotatingFileHandler(
        "logs/microblog.log", maxBytes=10240, backupCount=10
    )
    # message in the files: timestamp, logging level, message, source file, line num
    # uses a special format provided via logging.Formatter
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    # files will have only INFO level logs
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # lowering the app logger level to INFO too
    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog startup")
