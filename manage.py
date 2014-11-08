import os
from flask.ext.script import Manager
from app import app
from app.database import Base, engine, session
from app.models import User, POI, UserPOI
from getpass import getpass
from werkzeug.security import generate_password_hash


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@manager.command
def add_user():
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email already exists"
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
        password=generate_password_hash(password))
    session.add(user)
    session.commit()

@manager.command
def re_seed():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    lacma = POI(name="LACMA",
        category="arts",
        address="5905 Wilshire Blvd, Los Angeles, CA 90036",
        latitude=34.0629,
        longitude= -118.3578,
        desc="database test 1 description")
    venice = POI(name="Venice Beach Boardwalk",
        category="active",
        address="1800 Ocean Front Walk, Los Angeles, CA 90291",
        latitude=33.986,
        longitude= -118.473,
        desc="database test 2 description")
    barber = POI(name="The Blind Barber",
        category="drink",
        address="10797 Washington Blvd, Culver City, CA 90232",
        latitude=34.0153,
        longitude= -118.4073,
        desc="database test 3 description")
    jumbo = POI(name="Jumbo's Clown Room",
        category="other",
        address="5153 Hollywood Blvd, Hollywood, CA 90027",
        latitude=34.1017,
        longitude= -118.3023,
        desc="database test 4 description")
    baco = POI(name="Baco Mercat",
        category="food",
        address="408 S Main St, Los Angeles, CA 90013",
        latitude=34.0479,
        longitude= -118.2474,
        desc="database test 5 description")
    session.add_all([lacma, venice, barber, jumbo, baco])
    session.commit()

    user1 = User(username="test",
        email="test@gmail.com",
        password=generate_password_hash("test")
        )
    user2 = User(username="fake",
        email="fake@gmail.com",
        password=generate_password_hash("fake"))
    session.add_all([user1, user2])
    session.commit()

    user1.poi_assocs.append(UserPOI(poi=lacma, upvote=False))
    user1.poi_assocs.append(UserPOI(poi=venice, upvote=True))
    user2.poi_assocs.append(UserPOI(poi=venice, upvote=True))
    user2.poi_assocs.append(UserPOI(poi=baco, upvote=True))
    user2.poi_assocs.append(UserPOI(poi=barber, upvote=True))
    session.commit()

if __name__ == '__main__':
    manager.run()
