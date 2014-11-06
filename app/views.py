from flask import render_template, url_for

from app import app
from database import session
from models import User
from forms import LoginForm, RegistrationForm

@app.route('/login', methods=['GET'])
def login_get():
    form = LoginForm(request.args)
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def login_post():
    pass

@app.route('/register', methods=['GET'])
def register_get():
    form = RegistrationForm(request.args)
    return render_template('register.html', form=form)

@app.route('/register', methods=['POST'])
def register_post():
    form = RegistrationForm(request.form)
    if form.validate():
        if form.fname.data or form.lname.data:
            user = User(username=form.username.data,
                email=form.email.data,
                realname=form.fname.data+form.lname.data,
                password=form.password.data)
        else:
            user = User(username=form.username.data,
                email=form.email.data,
                password=form.password.data)
        session.add(user)
        session.commit()
        flash('Thanks for registering!', 'success')
        return redirect(url_for('login_get'))
    else:
        return render_template('register.html', form=form)
