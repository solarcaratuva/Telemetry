from datetime import datetime
from app import db 

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.types import JSON

Base = declarative_base()
Base.query = db.session.query_property()

class TestData(Base):
    __tablename__ = "TestData"

    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)
    run_id = Column(Integer)
    mph = Column(Integer)
    rpm = Column(Integer)
    miles = Column(Integer)
    soc = Column(Float)
    min_voltage = Column(Float)
    max_voltage = Column(Float)
    voltage = Column(Float)
    min_current = Column(Float)
    max_current = Column(Float)
    current = Column(Float)
    min_temperature = Column(Float)
    max_temperature = Column(Float)
    temperature = Column(Float)
    json = Column(JSON)


class Runs(Base):
    __tablename__ = 'Runs'
    run_id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    driver = Column(String)
    location = Column(String)
    description = Column(Text)
    timestamp = Column(DateTime, default = datetime.now)
