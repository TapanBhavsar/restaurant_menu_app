from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String, Column

table = declarative_base()

class User(table):
    __tablename__ = 'User'
    user_name = Column(String(30), primary_key = True)
    password = Column(String(16), nullable = False)
