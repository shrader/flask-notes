"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, URL, Optional, AnyOf

class AddUserForm(FlaskForm):
    """Form for adding pets."""

    username = StringField("Username", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField('Last Name',
        validators=[InputRequired()])
    email = StringField("Email",
        validators=[Email()])
    password = PasswordField("Password", validators=[InputRequired()])

