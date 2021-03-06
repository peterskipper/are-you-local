from wtforms import Form, TextField, TextAreaField, RadioField, PasswordField, validators

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

class POIForm(Form):
    name = TextField('Name', [validators.InputRequired()])
    category = RadioField('Category', choices=[('food', 'Food'), ('drink', 'Drink'),
        ('active', 'Active/Outdoors'), ('arts', 'Arts & Entertainment'), ('other', 'Other')])
    address = TextField('Address', [validators.InputRequired()])
    desc = TextAreaField('Description', [validators.InputRequired()],
        default='Tell users at least a sentence or two about this place!')
