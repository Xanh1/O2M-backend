from flask import Blueprint, jsonify, make_response, request
from controllers.controller_sensor import ControllerSensor
from .schemas.schemas_sensor import schema_save_sensor
from .schemas.schemas_sensor import schema_modify_sensor
from .schemas.schemas_sensor import schema_modify_Status_sensor
from controllers.auth import token_required

from flask_expects_json import expects_json
from controllers.utils.errors import Errors

url_sensor = Blueprint('url_sensor', __name__)
sensorC= ControllerSensor()
@token_required
@url_sensor.route('/listSensor')
def lista_sensor():
    return make_response(
        jsonify({"msg" : "OK", "code" : 200, "datos" : ([i.serialize for i in sensorC.listSensor()])}), 

        200
    )
    
@url_sensor.route('/saveSensor', methods = ["POST"])
@token_required
@expects_json(schema_save_sensor)
def save_sensor():
    data = request.json  
    c = sensorC.saveSensor(data=data)
    if c >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"tag": "datos guardados"}}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": Errors.error.get(str(c))}}),
            400
        )
        
@url_sensor.route('/modifySensor', methods = ["POST"])
@token_required
@expects_json(schema_modify_sensor)
def modifySensor():
    data = request.json  
    c = sensorC.modifySensor(data=data)
    if c >= 0:
        return make_response(
            jsonify({"msg": "DATOS CAMBIADOS CON EXITO", "code": 200, "datos": ["correcto"]}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": Errors.error.get(str(c))}}),
            400
        )
    
    
@url_sensor.route('/search/<uidS>')
@token_required
def search_by_uid(uidS):
    sensor = sensorC.search_sensor_by_uid(uidS=uidS)
    return make_response(
        #jsonify({"msg" : "OK", "code" : 200, "datos":personaC.buscarExternal(external).serialize}), 
        jsonify({"msg" : "OK", "code" : 200, "datos":[] if sensor == None else sensor.serialize}), 

        200
    )
        

@url_sensor.route('/searchName/<name>') #SE ENVIA EL NOMBRE SIN COMILLAS
@token_required
def search_by_name(name):
    sensor = sensorC.search_sensor_by_name(name).serialize
    if sensor:  
        return make_response(
        jsonify({"msg" : "OK", "code" : 200, "datos" : ([sensor])}), 
            200
        )
    else: 
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": "NO EXISTE"}}),
            400
        )
        
@url_sensor.route('/modify_status_Sensor/<uid>')
@token_required
def modify_status_Sensor(uid):
    c = sensorC.change_status(uid)
    if c >= 0:
        return make_response(
            jsonify({"msg": "ACTUALIZANDO ESTADO", "code": 200, "datos": {"external_id": uid}}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": Errors.error.get(str(c))}}),
            400
        )

@token_required
@url_sensor.route('/get/elements')
def list_allElements():
    return make_response(
        jsonify({"msg" : "OK", "code" : 200, "datos" : sensorC.list_element()}), 
        200
    )

