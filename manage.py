import os
from flask.ext.script import Manager
from app import app
from app.database import Base, engine, session
from app.models import User, POI, UserPOI
from getpass import getpass
from werkzeug.security import generate_password_hash
import random


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
        desc="Largest art museum in the western United States.  Check out the incredible Latin-American collection.")
    
    venice = POI(name="Venice Beach Boardwalk",
        category="active",
        address="1800 Ocean Front Walk, Los Angeles, CA 90291",
        latitude=33.986,
        longitude= -118.473,
        desc="Best people watching in the entire city.  Wander around, and get your fortune read by one of the palm readers.")
    
    barber = POI(name="The Blind Barber",
        category="drink",
        address="10797 Washington Blvd, Culver City, CA 90232",
        latitude=34.0153,
        longitude= -118.4073,
        desc="Hidden behind an actual barber shop, no sign.  Just walk straight through to the back, and delicious cocktails.")
    
    baco = POI(name="Baco Mercat",
        category="food",
        address="408 S Main St, Los Angeles, CA 90013",
        latitude=34.0479,
        longitude= -118.2474,
        desc="Try one of the amazing flatbread sandwiches!")

    dailypint = POI(name="The Daily Pint",
        category="drink",
        address="2310 Pico Blvd, Santa Monica, CA 90405",
        latitude=34.021084, 
        longitude= -118.466116,
        desc="Hole in the wall, casual and fun.  Start with the scotch.")

    brennans = POI(name="Brennan's Pub",
        category="drink",
        address="4089 Lincoln Blvd, Marina del Rey, CA 90292",
        latitude=33.988296, 
        longitude= -118.446087,
        desc="Turtle Racing.  Yes, seriously!")

    perch = POI(name="Perch",
        category="drink",
        address="448 S Hill St, Los Angeles, CA 90013",
        latitude=34.048858,
        longitude= -118.251316,
        desc="Rooftop bar with some amazing downtown views.  Great Happy Hour!")

    griffith = POI(name="Griffith Park",
        category="active",
        address="2800 E Observatory Rd, Los Angeles, CA 90027",
        latitude=34.118375,
        longitude= -118.300354,
        desc="Great hiking. Go with The Sierra Club on a night hike for some amazing views of the city, all lit up!")

    barnsdall = POI(name="Barnsdall Art Park",
        category="active",
        address="4800 Hollywood Blvd, Los Angeles, CA 90027",
        latitude=34.101528,
        longitude= -118.294334,
        desc="Great place for a picnic, or just a lazy Sunday afternoon.")

    firstfriday = POI(name="Abbot Kinney: First Friday",
        category="other",
        address="1121 Abbot Kinney Blvd, Venice, CA 90291",
        latitude=33.991867,
        longitude= -118.469779,
        desc="Shops and galleries open late in Abbot Kinney on the first Friday of each month.  Also, an amazing collection of food trucks!")

    cinespia = POI(name="Cinespia at Hollywood Forever",
        category="other",
        address="6000 Santa Monica Blvd, Los Angeles, CA 90038",
        latitude=34.090522,
        longitude= -118.319727,
        desc="Scary movies playing outdoors at Hollywood Forever Cemetery around Halloween. Bring a picnic!")

    timetravel = POI(name="Echo Park Time Travel Mart",
        category="other",
        address="1714 Sunset Blvd, Los Angeles, CA 90026",
        latitude=34.077282,
        longitude= -118.259066,
        desc="Quirky store for 'time travelers' in Echo Park. Profits fund the work of 826 Valencia, a nonprofit that focuses on writing education.")

    elmatador = POI(name="El Matador State Beach",
        category="active",
        address="32350 Pacific Coast Hwy, Malibu, CA 90265",
        latitude=34.039051,
        longitude= -118.875141,
        desc="Fewer services means fewer people. Head North toward Malibu to get away from the bustle near Santa Monica and contemplate the waves...")

    flower = POI(name="LA Flower Market",
        category="other",
        address="754 Wall St Los Angeles, CA 90014",
        latitude=34.040473,
        longitude= -118.24961,
        desc="Come early and see an incredible collection of flowers.  Avoid the crowds/bustle on Wednesdays and Fridays if you can.")
    
    largo = POI(name="Largo at the Coronet",
        category="arts",
        address="366 N La Cienega Blvd, Los Angeles, CA 90048",
        latitude=34.077871,
        longitude= -118.376322,
        desc="Both amazing live music and comedy.  Check out ongoing show 'The Thrilling Adventure Hour' for a good laugh!")

    hotelcafe = POI(name="The Hotel Cafe",
        category="arts",
        address="1623 N Cahuenga Blvd, Los Angeles, CA 90028",
        latitude=34.100437,
        longitude= -118.329829,
        desc="Tiny venue in Hollywood hosts some incredible bands that'll probably be famous in a couple years. For now, you can see them for $10!")

    noise = POI(name="A Noise Within",
        category="arts",
        address="3352 E Foothill Boulevard, Pasadena, CA 91107",
        latitude=34.149594,
        longitude= -118.081141,
        desc="Smaller Pasadena theater sticks to the classics.  And does an amazing job with them.")

    tsujita = POI(name="Tsujita",
        category="food",
        address="2057 Sawtelle Blvd, Los Angeles, CA 90025",
        latitude=34.039604, 
        longitude= -118.442753,
        desc="World's. Best. Noodles.  Omnomnomnom.")

    saffron = POI(name="Saffron & Rose",
        category="food",
        address="1387 Westwood Blvd, Los Angeles, CA 90024",
        latitude=34.055425,
        longitude= -118.4422,
        desc="Ice cream with amazing, unique flavors. Try the Cucumber, seriously!")

    kang = POI(name="Kang Ho-Dong Baekjeong",
        category="food",
        address="3465 W 6th St, Los Angeles, CA 90020",
        latitude=34.063733,
        longitude= -118.297282,
        desc="Amazing Korean BBQ in (of course) Koreatown. Knock back a Hite and order everything on the menu.")
    
    places_list = [lacma, venice, barber, baco, dailypint, brennans, 
        perch, griffith, barnsdall, firstfriday, cinespia, timetravel, 
        elmatador, flower, largo, hotelcafe, noise, tsujita, saffron, kang]

    session.add_all(places_list)
    session.commit()

    user1 = User(username="test",
        email="test@gmail.com",
        password=generate_password_hash("test")
        )

    session.add(user1)
    session.commit()

    for place in places_list:
        user1.poi_assocs.append(UserPOI(poi=place, upvote=1))

    session.commit()
    
    #Create sample users and upvotes
    for i in range(1, 20):
        username = "test" + str(i)
        email = "test" + str(i) + "@gmail.com"
        password = "test" + str(i)
        tempuser = User(username=username,
            email=email,
            password=generate_password_hash(password)
            )
        session.add(tempuser)
        session.commit()

        sampsize = random.randint(6, 12)
        sample_likes = random.sample(places_list, sampsize)
        for like in sample_likes:
            tempuser.poi_assocs.append(UserPOI(poi=like, upvote=1))

        session.commit()

if __name__ == '__main__':
    manager.run()
