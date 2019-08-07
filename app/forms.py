from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

