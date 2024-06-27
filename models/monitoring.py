import uuid
from datetime import datetime

from app import Base


class Monitoring(Base.Model):

    # table name
    __tablename__ = 'monitoring'

    # fields
    id         = Base.Column(Base.Integer, primary_key = True)
    uid        = Base.Column(Base.String(60), default = str(uuid.uuid4()), nullable = False)
    data       = Base.Column(Base.Float, nullable = False)
    start_date = Base.Column(Base.DateTime, nullable = False)
    end_date   = Base.Column(Base.DateTime, nullable = False)
    sensor_id  = Base.Column(Base.Integer, Base.ForeignKey('sensor.id'), nullable = False)
    
    # audit fields
    created_at = Base.Column(Base.DateTime, default = datetime.now)
    updated_at = Base.Column(Base.DateTime, default = datetime.now, onupdate = datetime.now)
    
    # child relationships
    sensor = Base.relationship("Sensor", back_populates="monitoring")
    
    # methods
    @property
    def serialize(self):
        return {
            'longitude'  : self.longitude,
            'latitude'   : self.latitude,
            'start_date' : self.start_date,
            'end_date'   : self.end_date,
            'data'       : self.data,
            'uid'        : self.uid,   
            'sensor_id': self.sensor.serialize
        }
    
    def copy(self):
    
        copy_monitoring = Monitoring(
            id         = self.id,
            uid        = self.uid,
            latitude   = self.latitude,
            longitude  = self.longitude,
            start_date = self.start_date,
            end_date   = self.end_date,
            data       = self.data,
            sensor_id  = self.sensor_id,
        )
    
        return copy_monitoring
    