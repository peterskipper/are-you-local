#import os.path

from flask import url_for
from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, Float, String, Sequence, ForeignKey, Table
from sqlalchemy.orm import relationship

from app import app
from database import Base, engine

class User(Base, UserMixin):
    """
    Domain model for a user
    """
    __tablename__ = 'user'

    #database fields
    id = Column(Integer, Sequence('user_id_sequence'), primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    realname = Column(String, nullable=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        print 'User id is {}, username is {}, user email is {} and user real name is {}'.format(self.id, self.username, self.email, self.realname)

# our many-to-many association table, in our domain model *before* POI class 
user_poi_table = Table('user_poi', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('poi_id', Integer, ForeignKey('poi.id'), nullable=False)
)

class POI(Base):
    """
    Domain model for a Point of Interest (POI)
    """
    __tablename__ = 'poi'

    #database fields
    id = Column(Integer, Sequence('poi_id_sequence'), primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    desc = Column(String, nullable=False)
    users = relationship('User', secondary=user_poi_table, backref='pois')

    def __repr__(self):
        print 'POI id is {}, name is {}, address is {}, latitude is {}, longitude is {}, and description is {}'.format(self.id, self.name, self.address, self.latitude, self.longitude, self.desc)

#CHECK: Is this the appropriate place to create tables?
Base.metadata.create_all(engine)