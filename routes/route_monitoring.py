from flask import Blueprint, jsonify, make_response, request
#from controllers.utils.errors import Errors
from flask_expects_json import expects_json
from controllers.utils.errors import Errors
from controllers.controller_monitoring import ControllerMonitoring
from .schemas.schemas_monitoring import schema_save
from datetime import datetime
from controllers.auth import token_required

url_monitoring = Blueprint('url_monitoring', __name__)


monitoringC = ControllerMonitoring()

#sirve para listar todos los monitores existentes 
@url_monitoring.route('/monitoring/list')
@token_required
def listMonitoring():
    return make_response(
        jsonify({"msg" : "OK", "code" : 200, "datos" : ([i.serialize for i in monitoringC.list()])}), 

        200
    )


#sirve para listar monitoreos con base a un intervalo de fecha 
@url_monitoring.route('/monitoring/list/date', methods=['GET'])
@token_required
def list_monitoring_within_date_range():
    data = request.json
    
    if data and 'start_date' in data and 'end_date' in data:
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
        
        controller = ControllerMonitoring()
        monitoring_within_range = controller.list_within_date_range(data)
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": [monitoring.serialize for monitoring in monitoring_within_range]}), 200)
    else:
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": Errors.error.get(str(m))}}),
            400
        )


#sirve para listar monitoreos con base a un intervalo de fecha y ademas un iteravalo de coordenadas 
@url_monitoring.route('/monitoring/list/date/location', methods=['GET'])
@token_required
def list_monitoring_within_date_and_location():
    data = request.json
    
    if data and 'start_date' in data and 'end_date' in data:
        controller = ControllerMonitoring()
        monitoring_within_range = controller.list_within_date_range(data)
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": [monitoring.serialize for monitoring in monitoring_within_range]}), 200)
    else:
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": Errors.error.get(str(m))}}),
            400
        )

#sirve para guardar monitoreso
@url_monitoring.route('/monitoring/save', methods = ["POST"])
@token_required
@expects_json(schema_save)
def saveMonitoring():
    data = request.json  # Supongamos que recibes los datos en formato JSON
    m = monitoringC.save(data)
    if m >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"tag": "datos guardados"}}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": Errors.error.get(str(m))}}),
            400
        )
    
#sirve para modifiacar monitreos ya existentes
@url_monitoring.route('/monitoring/modify/<uid>', methods=["POST"])
@token_required
@expects_json(schema_save)
def modifyMonitoring(uid):
    data = request.json
    result = monitoringC.modify(uid, data)
    
    if result >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"uid": uid}}),
            200
        )
    else:
        error_message = Errors.error.get(str(result))
        return make_response(
            jsonify({"msg": "ERROR", "code": 400, "datos": {"error": error_message}}),
            400
        )
