from flask import render_template, url_for, request, flash, redirect
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from database import session
from models import User
from forms import LoginForm, RegistrationForm, POIForm

# Helper func for the views with forms
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the {} field - {}".format(getattr(form, field).label.text, error), 'danger')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_get():
    form = LoginForm(request.args)
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    name = form.name.data
    password = form.password.data
    user = session.query(User).filter_by(username=name).first()
    if not user: # Try to find user via email
        user = session.query(User).filter_by(email=name).first()
    # If we STILL can't find user, or if password doesn't match, redirect
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username/email or password', 'danger')
        return redirect(url_for('login_get'))
    login_user(user)
    flash('Logged in successfully!', 'success')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index')) 

@app.route('/register', methods=['GET'])
def register_get():
    form = RegistrationForm(request.args)
    return render_template('register.html', form=form)

@app.route('/register', methods=['POST'])
def register_post():
    form = RegistrationForm(request.form)
    if form.validate():
        user = User(username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
                )
        if form.fname.data and form.lname.data:
            user.realname = form.fname.data + form.lname.data
        elif form.fname.data:
            user.realname = form.fname.data
        elif form.lname.data:
            user.realname = form.lname.data
        session.add(user)
        session.commit()
        flash('Thanks for registering!', 'success')
        return redirect(url_for('login_get'))
    else:
        flash_errors(form)
        return render_template('register.html', form=form)

@app.route('/add_poi', methods=['GET'])
def add_poi_get():
    form = POIForm(request.args, category=0)
    return render_template('add_poi.html', form=form)

@app.route('/add_poi', methods=['POST'])
def add_poi_post():
    form = POIForm(request.form)
