from datetime import datetime
from app import db 

from sqlalchemy import Boolean, Column 
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.types import JSON

Base = declarative_base()


class BMS(Base):
    __tablename__ = 'BMS'

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer)
    current = Column(Float)
    voltage = Column(Float)
    soc = Column(Float)
    max_temperature = Column(INTEGER(unsigned=True))
    temperature = Column(INTEGER(unsigned=True))
    charge_limit = Column(INTEGER(unsigned=True))
    discharge_limit = Column(INTEGER(unsigned=True))
    current_limit = Column(INTEGER(unsigned=True))
    disch_bool = Column(Boolean, default = False)
    charge_bool = Column(Boolean, default = False)
    safety_bool = Column(Boolean, default = False)
    malfunction = Column(Boolean, default = False)
    multi_purpose_out = Column(Boolean, default = False)
    always_on_signal = Column(Boolean, default = False)
    ready_signal = Column(Boolean, default = False)
    charge_signal = Column(Boolean, default = False)
    P0A1F = Column(Boolean, default = False)
    P0A00 = Column(Boolean, default = False)
    P0A80 = Column(Boolean, default = False)
    P0AFA = Column(Boolean, default = False)
    U0100 = Column(Boolean, default = False)
    P0A04 = Column(Boolean, default = False)
    P0AC0 = Column(Boolean, default = False)
    P0A01 = Column(Boolean, default = False)
    P0A02 = Column(Boolean, default = False)
    P0A03 = Column(Boolean, default = False)
    P0A81 = Column(Boolean, default = False)
    P0A9C = Column(Boolean, default = False)
    P0560 = Column(Boolean, default = False)
    P0AA6 = Column(Boolean, default = False)
    P0A05 = Column(Boolean, default = False)
    P0A06 = Column(Boolean, default = False)
    P0A07 = Column(Boolean, default = False)
    P0A08 = Column(Boolean, default = False)
    P0A09 = Column(Boolean, default = False)
    P0A0A = Column(Boolean, default = False)
    P0A0B = Column(Boolean, default = False)
    json = Column(JSON)

class KLS(Base):
    __tablename__ = 'KLS'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer)
    command_status = Column(Boolean, default = False)
    feedback_status = Column(Integer)
    hall_a = Column(Boolean, default = False)
    hall_b = Column(Boolean, default = False)
    hall_c = Column(Boolean, default = False)
    brake = Column(Boolean, default = False)
    backward = Column(Boolean, default = False)
    forward = Column(Boolean, default = False)
    foot = Column(Boolean, default = False)
    boost = Column(Boolean, default = False)
    rpm = Column(INTEGER(unsigned=True))
    current_limit_status = Column(Integer)
    voltage = Column(Integer)
    throttle = Column(Integer)
    controller_temp = Column(INTEGER(unsigned=True))
    motor_temp = Column(INTEGER(unsigned=True))
    timestamp = Column(DateTime, default = datetime.now)

class Runs(Base):
    __tablename__ = 'Runs'
    run_id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    driver = Column(String)
    location = Column(String)
    description = Column(Text)
    timestamp = Column(DateTime, default = datetime.now)
