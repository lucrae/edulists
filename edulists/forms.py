from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

from edulists import db
from edulists.models import User

class RegisterForm(FlaskForm):
    first_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=32)])
    last_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=32)])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=16)])
    accept_tos = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Get started')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # email has a clash
        if User.query.filter_by(email=self.email.data).first():
            self.email.errors.append('Sorry, this email address is already taken.')
            return False

        # first name has non-letter characters
        if not self.first_name.data.isalpha():
            self.first_name.errors.append('Please only use letters for your name.')
            return False

        # last name has non-letter characters
        if not self.last_name.data.isalpha():
            self.last_name.errors.append('Please only use letters for your name.')
            return False

        return True

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # account does not exist
        if not User.query.filter_by(email=self.email.data).first():
            self.email.errors.append('Sorry, this account does not exist.')
            return False

        # password is not correct
        if not User.query.filter_by(email=self.email.data).first().check_password(self.password.data):
            self.password.errors.append('Sorry, this password is incorrect.')
            return False

        return True