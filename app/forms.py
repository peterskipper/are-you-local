from wtforms import Form, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=3), 
        validators.InputRequired()])
    email = TextField('Email Address', [validators.Email(),
        validators.InputRequired()])
    fname = TextField('First Name')
    lname = TextField('Last Name')
    password = PasswordField('Password', [
            validators.InputRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    name = TextField('Username or Email', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
