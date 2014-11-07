#import os.path

from flask import url_for
from flask.ext.login import UserMixin
from sqlalchemy import Column, Boolean, Integer, Float, String, Sequence, ForeignKey, Table
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
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    realname = Column(String, nullable=True, default='')
    password = Column(String, nullable=False)
    pois = relationship('UserPOI', backref='user')

    def __repr__(self):
        return ('User id is {}, '
            'username is {}, '
            'user email is {}, '
            'user real name is {}, '
            'user password is {}'.format(
                self.id, 
                self.username, 
                self.email, 
                self.realname,
                self.password
                )
            )


class UserPOI(Base):
    __tablename__ = 'user_poi_association'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    poi_id = Column(Integer, ForeignKey('poi.id'), primary_key=True)
    upvote = Column(Boolean)
    poi = relationship('POI', backref='user_assocs')

class POI(Base):
    """
    Domain model for a Point of Interest (POI)
    """
    __tablename__ = 'poi'

    #database fields
    id = Column(Integer, Sequence('poi_id_sequence'), primary_key=True)
    name = Column(String, nullable=False)
    category = Column(Integer, nullable=False) 
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    desc = Column(String, nullable=False)

    def __repr__(self):
        print 'POI id is {}, name is {}, address is {}, latitude is {}, longitude is {}, and description is {}'.format(self.id, self.name, self.address, self.latitude, self.longitude, self.desc)

#CHECK: Is this the appropriate place to create tables? Remove Drop Tables
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)