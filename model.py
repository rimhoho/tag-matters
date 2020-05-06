from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///monthly_times_tags.db', echo=True)
Base = declarative_base()


class TimesTable(Base): 
    __tablename__ = 'times'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    tag = Column(String(255))
    periodeM = Column(String(25))
    frequency = Column(Integer)
    title = Column(String(255))
    date = Column(String(25))
    url = Column(String(255))
    img_URL = Column(String(255))

class GoogleTable(Base): 
    __tablename__ = 'google'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    trendDate = Column(PickleType)
    startDate = Column(String(25))
    endDate = Column(String(25))
    busiest = Column(String(25))
    trendIndex = Column(PickleType)
    fk_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    googleNTag = relationship('TimesTable')


class RedditTable(Base): 
    __tablename__ = 'reddit'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    tag = Column(String(255))
    createdDate = Column(String(25))
    postsCount = Column(Integer)
    vote = Column(Integer)
    # fk_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    # redditNTag = relationship('TimesTable')
    

TimesTable.__table__.create(bind=engine, checkfirst=True)
GoogleTable.__table__.create(bind=engine, checkfirst=True)
RedditTable.__table__.create(bind=engine, checkfirst=True)
