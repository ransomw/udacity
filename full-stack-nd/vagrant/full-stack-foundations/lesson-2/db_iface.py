from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base
from database_setup import Restaurant


_engine = create_engine(
    'sqlite:///restaurauntmenu.db')
Base.metadata.bind = _engine
_DBSession = sessionmaker(bind=_engine)
_session = _DBSession()

def get_restaurants():
    return _session.query(Restaurant).all()

def get_restaurant(id):
    return _session.query(Restaurant).filter_by(id=id).one()

def rename_restaurant(id, name):
    restaurant = _session.query(Restaurant).filter_by(id=id).one()
    restaurant.name = name
    _session.add(restaurant)
    _session.commit()

def delete_restaurant(id):
    restaurant = _session.query(Restaurant).filter_by(id=id).one()
    _session.delete(restaurant)
    _session.commit()

def new_restaurant(name):
    newRestaurant = Restaurant(name=name)
    _session.add(newRestaurant)
    _session.commit()
