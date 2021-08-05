from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from issues_blog.models import User

class RegisterForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, firstname):
        user = User.query.filter_by(firstname = firstname.data).first()
        if user:
            raise ValidationError('Username taken, please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email taken, please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReportForm(FlaskForm):
    title = StringField('Issue Title', validators=[DataRequired()])
    content = TextAreaField('Report Issue', validators=[DataRequired()])
    submit = SubmitField('Submit')