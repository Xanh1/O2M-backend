from datetime import datetime

from app import Base

person_sensor = Base.Table('person_sensor',
    Base.Column('person_id',  Base.Integer, Base.ForeignKey('person.id'), primary_key=True),
    Base.Column('sensor_id',  Base.Integer, Base.ForeignKey('sensor.id'), primary_key=True),
    Base.Column('created_at', Base.DateTime, nullable=False, default=datetime.now),
    Base.Column('updated_at', Base.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
)