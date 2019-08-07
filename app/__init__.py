from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# environment variables are in config.py
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models  # models are added in step 18.4 of Workflow.md

