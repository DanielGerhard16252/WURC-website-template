from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from server.forms.validators import Email, InvalidChars, StrongPassword
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    email = StringField('Email:', name="email", validators=[DataRequired(), Email(), InvalidChars()])
    password = PasswordField('Password:', name="password", validators=[DataRequired(), InvalidChars()])
    remember = BooleanField('Remember me', name="remember")
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    first_name = StringField('First name:', name="first_name", validators=[DataRequired(), InvalidChars()])
    last_name = StringField('Last name:', name="last_name", validators=[DataRequired(), InvalidChars()])
    email = StringField('Email:', name="email", validators=[DataRequired(), Email(), InvalidChars()])
    confirm_email = StringField('Confirm Email:', name="confirm_email", validators=[DataRequired(), Email(), InvalidChars(), EqualTo('email', message="Emails must match")])
    password = PasswordField('Password:', name="password", validators=[DataRequired(), InvalidChars(), StrongPassword()])
    confirm_password = PasswordField('Confirm Password:', name="confirm_password", validators=[DataRequired(), InvalidChars(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Submit')

class EmailForm(FlaskForm):
    email = StringField('Email: ', name="email", validators=[DataRequired(), Email(), InvalidChars()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    new_password = StringField('New password:', name="password", validators=[DataRequired(), InvalidChars(), StrongPassword()])
    confirm_new_password = StringField('Confirm password:', name="confirm_password", validators=[DataRequired(), InvalidChars(), EqualTo("password")])
    submit = SubmitField("Reset password")

class PasswordForm(FlaskForm):
    password = PasswordField('Password:', name="password", validators=[DataRequired(), InvalidChars()])
    submit = SubmitField('Submit')