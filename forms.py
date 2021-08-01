from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class RegisterForm(FlaskForm):
    inputFirstName = StringField('First name',
                                 [DataRequired(message="Please enter your first name")])
    inputLastName = StringField('Last name',
                                [DataRequired(message="Please enter your last name")])
    inputEmail = StringField('Email address',
                             [Email(message='Not a valid email address'),
                              DataRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password',
                                  [InputRequired(message="Please enter your password!"),
                                   EqualTo('inputConfirmPassword', message="Passwords does not match!!")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    inputEmail = StringField('Email address',
                             [Email(message="Not a valid email address"),
                              DataRequired(message="Please enter your email address!!!")])
    inputPassword = PasswordField('Password',
                                  [InputRequired(message="Please enter your password!!!")])
    submit = SubmitField('Login')
