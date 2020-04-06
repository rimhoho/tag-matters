from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *

engine = create_engine('sqlite:///monthly_times_tags.db')
Base = declarative_base()


class Times(Base): 
    __tablename__ = 'times'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    Category = Column(String(25))
    Tag = Column(String(255))
    Frequency = Column(String(255))
    Title = Column(String(255))
    Date = Column(String(25))
    Url = Column(String(255))
    img_URL = Column(String(255))

class Google(Base): 
    __tablename__ = 'google'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    Category = Column(String(25))
    Tag = Column(String(255))
    Interests_1 = Column(Integer)
    Interests_2 = Column(Integer)
    Interests_3 = Column(Integer)
    Interests_4 = Column(Integer)
    Interests_5 = Column(Integer)
    Interests_6 = Column(Integer)
    Interests_7 = Column(Integer)
    Interests_8 = Column(Integer)
    Interests_9 = Column(Integer)
    Interests_10 = Column(Integer)
    Interests_11 = Column(Integer)
    Interests_12 = Column(Integer)
    Interests_13 = Column(Integer)
    Interests_14 = Column(Integer)
    Interests_15 = Column(Integer)
    Interests_16 = Column(Integer)
    Interests_17 = Column(Integer)
    Interests_18 = Column(Integer)
    Interests_19 = Column(Integer)
    Interests_20 = Column(Integer)

Times.__table__.create(bind=engine, checkfirst=True)
Google.__table__.create(bind=engine, checkfirst=True)
