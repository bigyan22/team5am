from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import Email, DataRequired, EqualTo, Length


class ContactFrom (FlaskForm):
    name = StringField(label="Your Name:", validators=[DataRequired()])
    email_address = EmailField(label='Email Address: ', validators=[DataRequired(), Email()])

    phone = StringField(label="Phone Number",validators=[DataRequired()])
    description = TextAreaField(label="Feedback", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Login")



class RegisterForm(FlaskForm):
    username = StringField(label='User Name: ', validators=[DataRequired(), Length(min=3, max=15)])
    email = EmailField(label='Email Address: ', validators=[DataRequired(), Email()])
    password1 = PasswordField(label='Password: ', validators=[DataRequired(),Length(min=4, max=8)])
    password2 = PasswordField(label='Confirm Password: ', validators=[
        DataRequired(),
        EqualTo('password1', message='Passwords must match!')
    ])
    
    submit = SubmitField(label='Create Account')
