from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import *
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///monthly_times_tags.db', echo=False)
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
    busiest = Column(String(25))
    trendIndex = Column(PickleType)
    fk_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    googleNTag = relationship('TimesTable')


# class RedditTable(Base): 
#     __tablename__ = 'reddit'
#     __table_args__ = {'extend_existing': True}

#     id = Column(Integer, primary_key=True)
#     tag = Column(String(255))
#     commentsCount = Column(Integer)
    
    # fk_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    # redditNTag = relationship('TimesTable')
    
class YoutubeTable(Base): 
    __tablename__ = 'youtube'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    tag = Column(String(255))
    url = Column(String(255))
    title = Column(String(255))
    img_url = Column(String(255))
    viewCount = Column(Integer)
    commentCount = Column(Integer)
    likeCount = Column(Integer)

class TagByPeriodeTable(Base):
    __tablename__ = 'tagByPeriode'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    periodeM = Column(String(25))
    tagArr_per_month = Column(PickleType)

TimesTable.__table__.create(bind=engine, checkfirst=True)
GoogleTable.__table__.create(bind=engine, checkfirst=True)
# RedditTable.__table__.create(bind=engine, checkfirst=True)
YoutubeTable.__table__.create(bind=engine, checkfirst=True)
TagByPeriodeTable.__table__.create(bind=engine, checkfirst=True)