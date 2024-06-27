from app import Base
from models.sensor import Sensor
from models.person import Person
from models.element_type import ElementType
import uuid
from app import Base
import  re
class ControllerSensor():

    def listSensor(self):
        return Sensor.query.all()
    


    def validate_Ip(self, ip):
        exp_ipv4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        if re.match(exp_ipv4, ip):
            return True
        else:
            return False



    def saveSensor(self,data):
        sensor= Sensor()
        person = Person.query.filter_by(uid=data["person"]).first()
        if person:
            if self.validate_Ip(data['ip']):
                sensor.ip = data['ip']
                sensor.element_type = data['element_type']            
                sensor.name = data['name']

                sensor.status = True
                #sensor.uid = uuid.uuid4

            
                #sensor.person_id= person.id
                Base.session.add(sensor)
                sensor.people.append(person)
                Base.session.commit()
                return sensor.id
            else:
                return -16
        else:
            return -11



    def modifySensor(self, data):
        sensor = Sensor.query.filter_by(uid=data['uid']).first()
        if sensor is None:
            return -12
        else:
            if self.validate_Ip(data['ip']):
                new_sensor = sensor.copy()
                new_sensor.name = data.get('name', sensor.name)
                new_sensor.element_type = data.get('element_type', sensor.element_type)
                new_sensor.ip = data.get('ip', sensor.ip)
                new_sensor.people = sensor.people  # Ensure `sensor.people` is not a set
                new_sensor.uid = uuid.uuid4()
                Base.session.merge(new_sensor)
                Base.session.commit()
                return new_sensor.id
            else:
                return -16
        
        
    
    def change_status(self,uid):
        sensor= Sensor.query.filter_by(uid=uid).first()
        if sensor is None:
            return -12
        else:
            new_sensor= sensor.copy()
            if new_sensor.status == True:
                new_sensor.status= False
                new_sensor.uid= uuid.uuid4()
                Base.session.merge(new_sensor)
                Base.session.commit()
            else:
                new_sensor.status= True
                new_sensor.uid= uuid.uuid4()
                Base.session.merge(new_sensor)
                Base.session.commit()
        return new_sensor.id


    def search_sensor_by_uid(self, uidS):
        sensor = Sensor.query.filter_by(uid=uidS).first()
        if sensor:
            return sensor
        else:
            return None

    def search_sensor_by_name(self, sensor_name):
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        return sensor
    
    
            


            
             
            
    def list_element(self):
        return ElementType.list()

        