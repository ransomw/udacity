from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base
from database_setup import Restaurant
from database_setup import MenuItem

engine = create_engine(
    'sqlite:///restaurauntmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Greasy Joe")
session.add(myFirstRestaurant)
session.commit()
print session.query(Restaurant).all()

