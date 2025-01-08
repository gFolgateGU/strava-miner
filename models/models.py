from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    strava_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    strava_token = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    activities = relationship("Activity", back_populates="user")

class Activity(Base):
    __tablename__ = 'activities'
    activity_id = Column(BigInteger, primary_key=True)
    strava_id = Column(BigInteger, ForeignKey('users.strava_id'))
    name = Column(String(255))
    distance = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    total_elevation_gain = Column(Float)
    type = Column(String(50))
    start_date = Column(DateTime)
    start_date_local = Column(DateTime)
    average_speed = Column(Float)
    max_speed = Column(Float)
    average_cadence = Column(Float, nullable=True)
    average_heartrate = Column(Float, nullable=True)
    max_heartrate = Column(Float, nullable=True)
    user = relationship("User", back_populates="activities")
