from models.monitoring import Monitoring
from models.sensor import Sensor

from models.sensor import Sensor
from sqlalchemy import and_, extract, func
import uuid
from app import Base
from datetime import datetime
from models.element_type import ElementType  # Asegúrate de que esta línea está presente


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

    def obtener_promedio_calidad_por_dia_air(self):
        # Crear una lista con los nombres de los meses en español
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Inicializar un diccionario para almacenar los promedios por día
        promedios_por_dia = {}

        # Obtener solo los sensores de tipo aire
        sensores_aire = Sensor.query.filter(Sensor.element_type == ElementType.AIR).all()
        sensor_ids = [sensor.id for sensor in sensores_aire]

        # Obtener solo los registros de monitoring que correspondan a los sensores de aire
        registros = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids)).all()

        # Iterar sobre cada registro y agrupar los datos por año, mes y día
        for registro in registros:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_por_dia:
                promedios_por_dia[(año, mes, dia)] = []

            promedios_por_dia[(año, mes, dia)].append(registro.data)

        # Inicializar una lista vacía para los resultados
        resultados = []

        # Calcular el promedio para cada día y construir la estructura deseada
        for (año, mes, dia), datos in promedios_por_dia.items():
            promedio = sum(datos) / len(datos)

            resultado_dia = {
                "promedioCalidadDato": promedio,
                "año": año,
                "mes": mes,
                "dia": dia,
                "nombre": nombres_meses[mes - 1]
            }

            resultados.append(resultado_dia)

        return resultados
    
    def obtener_promedio_calidad_por_dia_water(self):
        # Crear una lista con los nombres de los meses en español
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Inicializar un diccionario para almacenar los promedios por día
        promedios_por_dia = {}

        # Obtener solo los sensores de tipo aire
        sensores_aire = Sensor.query.filter(Sensor.element_type == ElementType.WATER).all()
        sensor_ids = [sensor.id for sensor in sensores_aire]

        # Obtener solo los registros de monitoring que correspondan a los sensores de aire
        registros = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids)).all()

        # Iterar sobre cada registro y agrupar los datos por año, mes y día
        for registro in registros:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_por_dia:
                promedios_por_dia[(año, mes, dia)] = []

            promedios_por_dia[(año, mes, dia)].append(registro.data)

        # Inicializar una lista vacía para los resultados
        resultados = []

        # Calcular el promedio para cada día y construir la estructura deseada
        for (año, mes, dia), datos in promedios_por_dia.items():
            promedio = sum(datos) / len(datos)

            resultado_dia = {
                "promedioCalidadDato": promedio,
                "año": año,
                "mes": mes,
                "dia": dia,
                "nombre": nombres_meses[mes - 1]
            }

            resultados.append(resultado_dia)

        return resultados
    
#Tanto de agua como de air
    def obtener_promedios_calidad_por_dia(self):
        # Crear una lista con los nombres de los meses en español
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Inicializar los diccionarios para almacenar los promedios por día
        promedios_aire = {}
        promedios_agua = {}

        # Obtener los sensores de tipo aire
        sensores_aire = Sensor.query.filter(Sensor.element_type == ElementType.AIR).all()
        sensor_ids_aire = [sensor.id for sensor in sensores_aire]

        # Obtener los registros de monitoring que correspondan a los sensores de aire
        registros_aire = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids_aire)).all()

        # Calcular promedios para sensores de aire
        for registro in registros_aire:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_aire:
                promedios_aire[(año, mes, dia)] = []

            promedios_aire[(año, mes, dia)].append(registro.data)

        # Obtener los sensores de tipo agua
        sensores_agua = Sensor.query.filter(Sensor.element_type == ElementType.WATER).all()
        sensor_ids_agua = [sensor.id for sensor in sensores_agua]

        # Obtener los registros de monitoring que correspondan a los sensores de agua
        registros_agua = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids_agua)).all()

        # Calcular promedios para sensores de agua
        for registro in registros_agua:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_agua:
                promedios_agua[(año, mes, dia)] = []

            promedios_agua[(año, mes, dia)].append(registro.data)

        # Inicializar la estructura final para el resultado
        resultados = {
            "aire": [],
            "agua": []
        }

        # Calcular el promedio para aire
        for (año, mes, dia), datos in promedios_aire.items():
            promedio = sum(datos) / len(datos)
            resultado_dia = {
                "promedioCalidadDato": promedio,
                "año": año,
                "mes": mes,
                "dia": dia,
            }
            resultados["aire"].append(resultado_dia)

        # Calcular el promedio para agua
        for (año, mes, dia), datos in promedios_agua.items():
            promedio = sum(datos) / len(datos)
            resultado_dia = {
                "promedioCalidadDato": promedio,
                "año": año,
                "mes": mes,
                "dia": dia,
            }
            resultados["agua"].append(resultado_dia)

        return resultados

