from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String, Column

table = declarative_base()

class Restaurant(table):
    __tablename__ = 'Restaurant'
    name = Column(String(50), primary_key = True)
