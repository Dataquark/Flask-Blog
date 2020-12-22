from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):

    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


# Step 40 in the Workflow
class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already chosen")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Email is already chosen")


class EditProfileForm(FlaskForm):
    # Step 53 in the Workflow
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        # we are passing the args, kwargs of this class to its parent class
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # super().__init__(*args, **kwargs) in Python 3
        self.original_username = original_username

    def validate_username(self, username):
        # we check if the new entered name is not equal to what we have in db
        if username.data != self.original_username:
            # if so, we check if the new entered name exist in db
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                # if new chosen name is the same as in our db, we raise an error
                raise ValidationError("Username taken! Please use different one!")


# Follow and unfollowing actions, step 69
class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")
