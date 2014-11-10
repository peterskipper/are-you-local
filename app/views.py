import urllib
import json
import decimal
from flask import render_template, url_for, request, flash, redirect
from flask.ext.login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from database import session
from models import User, POI
from forms import LoginForm, RegistrationForm, POIForm

# Helper func for the views with forms
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the {} field - {}".format(getattr(form, field).label.text, error), 'danger')

#Helper func to get Lat/Long from address
def geocode(address):
    address = urllib.quote_plus(address)
    print address
    request = ("http://maps.googleapis.com/maps/api/geocode/json?address={}&"
        "sensor=false".format(address))
    data = json.loads(urllib.urlopen(request).read())
    print data
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return decimal.Decimal(lat), decimal.Decimal(lng)
    else:
        return '',''

@app.route('/')
def index():
    poi_list =[]
    pois = session.query(POI).all()
    for poi in pois:
        poi_list.append(poi.as_dictionary())

    visited_list = []
    if current_user.is_authenticated:
        user = session.query(User).get(int(current_user.get_id()))
        for assoc in user.poi_assocs:
            visited_list.append(assoc.poi_id)
    return render_template('index.html', poi_list=json.dumps(poi_list),
        visited_list=json.dumps(visited_list))

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
    if form.validate():
        lat, lng = geocode(form.address.data)
        if lat and lng:
            poi = POI(name=form.name.data,
                category=form.category.data,
                address=form.address.data,
                latitude=lat,
                longitude=lng,
                desc=form.desc.data)
            session.add(poi)
            session.commit()
            flash('You added a new place!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Google Maps could not find that address. Try again!',
                'warning')
            return render_template('add_poi.html', form=form)

    else:
        flash_errors(form)
        return render_template('add_poi.html', form=form)
