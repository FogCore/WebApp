from WebApp import APIGateway
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Regexp('^\w+$', message='Username can only contain letters, numbers and underscores.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        response = APIGateway.User.check_user_existence(username=username.data)
        json = response.json()
        if response.status_code == 200:
            raise ValidationError('That username is taken. Please choose a different one.')
        elif response.status_code == 404:
            return
        else:
            raise ValidationError(json['message'])


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^\w+$', message='Username can only contain letters, numbers and underscores.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CloudletsFindForm(FlaskForm):
    id = StringField('ID')
    name = StringField('Name')
    cpu_cores = IntegerField('CPU cores')
    cpu_frequency = FloatField('CPU frequency')
    ram_size = IntegerField('RAM')
    rom_size = IntegerField('ROM')
    os = StringField('Operating system')
    os_kernel = StringField('OS kernel')
    ip = StringField('IP address')
    latitude = FloatField('Latitude')
    longitude = FloatField('Longitude')
    city = StringField('City')
    country = StringField('Country')
    region = StringField('Region')
    submit = SubmitField('Start')
