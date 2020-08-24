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

class GoogleBTable(Base): 
    __tablename__ = 'google'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    busiest = Column(String(25))
    fk_b_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    googleNTag = relationship('TimesTable')

class GoogleDTable(Base): 
    __tablename__ = 'google'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    trendDate = Column(Date)
    fk_d_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    googleNTag = relationship('TimesTable')

class GoogleITable(Base): 
    __tablename__ = 'google'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    trendIndex = Column(Integer)
    fk_i_times = Column(Integer, ForeignKey("times.id", ondelete='CASCADE'), nullable=False)
    googleNTag = relationship('TimesTable')

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

# class TagByPeriodeTable(Base):
#     __tablename__ = 'tagByPeriode'
#     __table_args__ = {'extend_existing': True}

#     id = Column(Integer, primary_key=True)
#     periodeM = Column(String(25))
#     tagArr_per_month = Column(PickleType)

TimesTable.__table__.create(bind=engine, checkfirst=True)
GoogleBTable.__table__.create(bind=engine, checkfirst=True)
GoogleDTable.__table__.create(bind=engine, checkfirst=True)
GoogleITable.__table__.create(bind=engine, checkfirst=True)
YoutubeTable.__table__.create(bind=engine, checkfirst=True)
# TagByPeriodeTable.__table__.create(bind=engine, checkfirst=True)