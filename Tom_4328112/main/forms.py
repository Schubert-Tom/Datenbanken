from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .db_models import User


##########################   Login  ##########################
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Choose another one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Choose another one!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    # this module describes how differnt user input forms are created.
    # With the package wtf-forms it is possible to configure these in python code and 
    # add validations with for the forms combined with sql_alchemy

##########################   Chat  ##########################

class CreateChat(FlaskForm):
    chat_name= StringField('Chat name', validators=[DataRequired(), Length(min=2, max=20)])
    participants= StringField('Add to Chat', validators=[Length(min=2, max=20)])
    create = SubmitField('create')