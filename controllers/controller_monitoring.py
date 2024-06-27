from models.monitoring import Monitoring
from models.sensor import Sensor
from sqlalchemy import and_
import uuid
from app import Base
from datetime import datetime

class ControllerMonitoring:

    def list(self):
        return Monitoring.query.all()
    
    def list_within_date_range(self, data):
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")
        return Monitoring.query.filter(and_(Monitoring.start_date >= start_date, Monitoring.end_date <= end_date)).all()

    def save(self, data):
        monitoring = Monitoring()

        sensor_uid = data.get("uid") 
        sensor = Sensor.query.filter_by(uid=sensor_uid).first()
        
        if sensor:
            if data.get("start_date") and data.get("end_date"):
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
                
                if end_date >= start_date:
                    monitoring.latitude = data['latitude']
                    monitoring.longitude = data['longitude']
                    monitoring.start_date = start_date
                    monitoring.end_date = end_date
                    monitoring.data = float(data['data'])  # Convertir data a float
                    monitoring.uid = uuid.uuid4()

                    monitoring.sensor_id = sensor.id
                    Base.session.add(monitoring)
                    Base.session.commit()
                    return monitoring.id
                else:
                    return -1  # La fecha de finalización es anterior a la fecha de inicio
            else:
                return -2  # Las fechas no están presentes en los datos
        else:
            return -3 # No se encontró el sensor con el uid proporcionado        



    def modify(self, uid, data):
        # Recuperar el censo existente de la base de datos utilizando external_id
        monitoring = Monitoring.query.filter_by(uid = uid).first()
        
        if monitoring is None:
            return -4  # 
        
        # Hacer una copia del censo existente
        new_monitoring = monitoring.copy()
        
        sensor_uid = data.get("uid")
        sensor = Sensor.query.filter_by(uid=sensor_uid).first()
                
        if sensor:
            if data["start_date"] and data["end_date"]:
                start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
                        
                if end_date > start_date:
                    monitoring.uid = data['uid']
                    monitoring.latitude = data['latitude']
                    monitoring.longitude = data['longitude']
                    monitoring.start_date = data['start_date']
                    monitoring.end_date = data['end_date']
                    monitoring.data = data['data']
                    monitoring.sensor_id = sensor.id
                    Base.session.merge(monitoring)
                    Base.session.commit()
                    return monitoring.id

                else:
                    return -1  # Código de error para indicar que la fecha de fin no es posterior a la fecha de inicio
        else:
            return -5  # Código de error para indicar que no se ingresó fecha de inicio


    



