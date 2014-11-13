import urllib
import json
import decimal
from sqlalchemy import func
from flask import render_template, url_for, request, flash, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from database import session, engine
from models import User, POI, UserPOI
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
    request = ("http://maps.googleapis.com/maps/api/geocode/json?address={}&"
        "sensor=false".format(address))
    data = json.loads(urllib.urlopen(request).read())
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return decimal.Decimal(lat), decimal.Decimal(lng)
    else:
        return '',''

@app.route('/', methods=["GET"])
def index():
    pois = session.query(POI).order_by(POI.id).all()

    # Add in User info, if applicable
    user_dict = {}
    if not current_user.is_anonymous():
        tuples = session.query(UserPOI.poi_id, UserPOI.upvote).filter_by(
            user_id = int(current_user.get_id())).order_by(UserPOI.poi_id)
        for key, val in tuples:
            user_dict[key] = val
    
    poi_list =[]
    for poi in pois:
        entry = poi.as_dictionary()
        entry["visited"] = poi.id in user_dict
        entry["upvote"] = user_dict[poi.id] if poi.id in user_dict else None
        poi_list.append(entry)

    return render_template('index.html', poi_list=json.dumps(poi_list))


@app.route('/', methods=['POST'])
@login_required
def index_post():
    upvote = int(request.form['upvote'])
    user = session.query(User).get(int(current_user.get_id()))
    poi = session.query(POI).get(int(request.form['poi_id']))
    user.poi_assocs.append(UserPOI(poi=poi, upvote=upvote))
    session.commit()
    return redirect(url_for('index'))
    

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
@login_required
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
@login_required
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
            user = session.query(User).get(int(current_user.get_id()))
            user.poi_assocs.append(UserPOI(poi=poi, upvote=1))
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

@app.route('/top_ten')
def top_ten():
    result = session.query(POI.id, POI.category, POI.name, func.sum(UserPOI.upvote)
        ).join(UserPOI).group_by(POI.id).order_by(POI.id)
        
    # Add in User info, if applicable
    user_visited = []
    if not current_user.is_anonymous():
        user = session.query(User).get(int(current_user.get_id()))
        for assoc in user.poi_assocs:
            user_visited.append(assoc.poi_id)

    poi_list = []
    for row in result:
        entry = {
            "id": row[0],
            "category": row[1],
            "name": row[2],
            "total_upvotes": row[3],
            "visited": row[0] in user_visited
        }
        poi_list.append(entry)

    # Sort and return the Top Ten
    top_ten = sorted(poi_list, 
        key=lambda k: k['total_upvotes'], 
        reverse=True)[:10]  
    return render_template('top_ten.html', top_ten=top_ten)

@app.route('/all_pois')
def all_pois():
    pois = session.query(POI.id, POI.name, POI.category, POI.address).order_by(POI.id).all()

    # Add in User info, if applicable
    user_dict = {}
    if not current_user.is_anonymous():
        tuples = session.query(UserPOI.poi_id, UserPOI.upvote).filter_by(
            user_id = int(current_user.get_id())).order_by(UserPOI.poi_id)
        for key, val in tuples:
            user_dict[key] = val

    poi_list =[]
    for poi in pois:
        entry = {
            "id": poi.id,
            "name": poi.name,
            "category": poi.category,
            "address": poi.address,
            "visited": poi.id in user_dict,
            "upvote": user_dict[poi.id] if poi.id in user_dict else None
        }
        poi_list.append(entry)

    return render_template('all_pois.html', poi_list=poi_list)
    


