from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# environment variables are in config.py
# This is step 18 in the Workflow.md
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# This is step 28 in the Workflow.md
login = LoginManager(app)
login.login_view = "login"  # Step 35 in the Workflow

from app import routes, models  # models are added in step 18.4 of Workflow.md

