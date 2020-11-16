# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship


from database_lib.tables.restaurant import Restaurant, table

# table = declarative_base()

class MenuItem(table):
    __tablename__ = 'MenuItem'
    name = Column(String(50), primary_key=True)
    description = Column(String(200))
    course = Column(String(20), nullable=False)
    price = Column(String(8), nullable=False)
    restaurant_name = Column(String(50), ForeignKey('Restaurant.name'))
    # restaurant = relationship(Restaurant)
