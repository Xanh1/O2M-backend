from models.monitoring import Monitoring
from models.sensor import Sensor

from models.sensor import Sensor
from sqlalchemy import and_, extract, func
import uuid
from app import Base
from datetime import datetime
from models.element_type import ElementType  # Asegúrate de que esta línea está presente
import requests
from numpy.polynomial import Polynomial
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


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

#estos valeeeeeeeeen para la grafica

    def obtener_promedio_calidad_por_dia_air(self):
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        promedios_por_dia = {}

        sensores_aire = Sensor.query.filter(Sensor.element_type == ElementType.AIR).all()
        sensor_ids = [sensor.id for sensor in sensores_aire]

        registros = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids)).all()

        for registro in registros:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_por_dia:
                promedios_por_dia[(año, mes, dia)] = []

            promedios_por_dia[(año, mes, dia)].append(registro.data)

        resultados = []

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

        resultados_ordenados = sorted(resultados, key=lambda x: (x["año"], x["mes"], x["dia"]))

        return resultados_ordenados

        
#estos valeeeeeeeeen para la grafica
    def obtener_promedio_calidad_por_dia_water(self):
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        promedios_por_dia = {}

        sensores_agua = Sensor.query.filter(Sensor.element_type == ElementType.WATER).all()
        sensor_ids = [sensor.id for sensor in sensores_agua]

        registros = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids)).all()

        for registro in registros:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_por_dia:
                promedios_por_dia[(año, mes, dia)] = []

            promedios_por_dia[(año, mes, dia)].append(registro.data)

        resultados = []

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

        resultados_ordenados = sorted(resultados, key=lambda x: (x["año"], x["mes"], x["dia"]))

        return resultados_ordenados

    

    
#Tanto de agua como de air
    def obtener_promedios_calidad_por_dia(self):
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        promedios_aire = {}
        promedios_agua = {}

        sensores_aire = Sensor.query.filter(Sensor.element_type == ElementType.AIR).all()
        sensor_ids_aire = [sensor.id for sensor in sensores_aire]

        registros_aire = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids_aire)).all()

        for registro in registros_aire:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_aire:
                promedios_aire[(año, mes, dia)] = []

            promedios_aire[(año, mes, dia)].append(registro.data)

        sensores_agua = Sensor.query.filter(Sensor.element_type == ElementType.WATER).all()
        sensor_ids_agua = [sensor.id for sensor in sensores_agua]

        registros_agua = Monitoring.query.filter(Monitoring.sensor_id.in_(sensor_ids_agua)).all()

        for registro in registros_agua:
            fecha = registro.start_date
            año = fecha.year
            mes = fecha.month
            dia = fecha.day

            if (año, mes, dia) not in promedios_agua:
                promedios_agua[(año, mes, dia)] = []

            promedios_agua[(año, mes, dia)].append(registro.data)

        resultados = {
            "aire": [],
            "agua": []
        }

        for (año, mes, dia), datos in promedios_aire.items():
            promedio = sum(datos) / len(datos)
            resultado_dia = {
                "promedioCalidadDato": promedio,
                "año": año,
                "mes": mes,
                "dia": dia,
            }
            resultados["aire"].append(resultado_dia)

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


#Mrtodo para la extrapolacion de aire
    def extrapolar_calidad_para_fecha_aire(self, dia, mes, año, grado=1):
        url = "http://127.0.0.1:5000/monitoring/promedio/por-dia/aire"
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
        except requests.RequestException as e:
            return {"msg": f"Error en la solicitud a {url}: {str(e)}", "code": 500}

        if json_data['code'] != 200:
            return {"msg": "Error al obtener los datos de calidad del agua", "code": 400}
        
        datos = json_data['datos']
        
        datos_filtrados = [d for d in datos if d['mes'] == mes]
        
        if len(datos_filtrados) < 3:
            return {"msg": "No hay datos suficientes para extrapolación", "code": 400}

        dias = []
        calidad_datos = []
        for d in datos_filtrados:
            if 'dia' in d and 'promedioCalidadDato' in d:
                dias.append(d['dia'])
                calidad_datos.append(d['promedioCalidadDato'])
        
        if len(dias) < 1 or len(calidad_datos) < 1:
            return {"msg": "No hay datos suficientes para extrapolación", "code": 400}

        try:
            calidad_extrapolada = calidad_datos[0]
            for i in range(1, len(dias)):
                p = Polynomial.fit(dias[:i+1], calidad_datos[:i+1], grado)
                calidad_extrapolada = p(dias[i])
        except np.linalg.LinAlgError:
            return {"msg": "Error numérico en el ajuste del polinomio", "code": 500}

        resultado = {
            "año": año,
            "dia": dia,
            "mes": f"{nombres_meses[mes - 1]}",  # Añadir el nombre del mes y el número del mes
            "valorExtrapolado": calidad_extrapolada
        }

        return {"msg": "OK", "code": 200, "datos": resultado}
#Método para la extrapolación de agua
    def extrapolar_calidad_para_fecha_agua(self, dia, mes, año, grado=1):
        url = "http://127.0.0.1:5000/monitoring/promedio/por-dia/agua"
        nombres_meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
        except requests.RequestException as e:
            return {"msg": f"Error en la solicitud a {url}: {str(e)}", "code": 500}

        if json_data['code'] != 200:
            return {"msg": "Error al obtener los datos de calidad del agua", "code": 400}
        
        datos = json_data['datos']
        
        datos_filtrados = [d for d in datos if d['mes'] == mes]
        
        if len(datos_filtrados) < 3:
            return {"msg": "No hay datos suficientes para extrapolación", "code": 400}

        dias = []
        calidad_datos = []
        for d in datos_filtrados:
            if 'dia' in d and 'promedioCalidadDato' in d:
                dias.append(d['dia'])
                calidad_datos.append(d['promedioCalidadDato'])
        
        if len(dias) < 1 or len(calidad_datos) < 1:
            return {"msg": "No hay datos suficientes para extrapolación", "code": 400}

        try:
            calidad_extrapolada = calidad_datos[0]
            for i in range(1, len(dias)):
                p = Polynomial.fit(dias[:i+1], calidad_datos[:i+1], grado)
                calidad_extrapolada = p(dias[i])
        except np.linalg.LinAlgError:
            return {"msg": "Error numérico en el ajuste del polinomio", "code": 500}

        resultado = {
            "año": año,
            "mes": mes,
            "dia": dia,
            "nombre": nombres_meses[mes - 1],  # Añadir el nombre del mes
            "calidadExtrapolada": calidad_extrapolada
        }

        return {"msg": "OK", "code": 200, "datos": resultado}
