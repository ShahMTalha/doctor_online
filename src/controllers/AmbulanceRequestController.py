from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import ambulance_bp, patient_bp

from src.models.AmbulanceDetailModel import AmbulanceDetailModel
from src.models.AmbulanceRequestModel import AmbulanceRequestModel
from src.models.AmbulanceRequestDetailsModel import AmbulanceRequestDetailsModel


@ambulance_bp.route('/get_nearby_ambulance', methods=['GET'])
@Authentication.decode_auth_token
def get_nearby_ambulance():
    try:
        lat = request.args.get('lat', '')
        long = request.args.get('long', '')
        offset = request.args.get('offset', '')
        limit = request.args.get('limit', '')
        own_id = request.args.get('own_id', '')
        db_data = AmbulanceDetailModel.get_ambulance_by_location(lat, long, offset, limit, own_id)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'user_id': each.user_id,
                    'name': each.name,
                    'email': each.email,
                    'address': each.address,
                    'distance': each.distance,
                    'latitude': each.latitude,
                    'longitude': each.longitude,
                    'image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.lab_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/add_ambulance_request', methods=['POST'])
@Authentication.decode_auth_token
def add_ambulance_request():
    try:
        patient = request.form['patient']
        source = request.form['source']
        destination = request.form['destination']
        description = request.form['description']
        ambulance = AmbulanceRequestModel(patient, source, destination, description)
        ambulance.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=ambulance.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/update_ambulance_request', methods=['POST'])
@Authentication.decode_auth_token
def update_ambulance_request():
    try:
        ambulance_request_id = request.form.get('ambulance_request_id', "")
        data_to_update = {
            "source": request.form.get('source', ""),
            "destination": request.form.get('destination', ""),
            "description": request.form.get('description', ""),
            "status": request.form.get('status', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        AmbulanceRequestModel.update_by_id(ambulance_request_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/get_ambulance_request', methods=['GET'])
@Authentication.decode_auth_token
def get_ambulance_request():
    try:
        name = request.args.get('name', '')
        user_id = request.args.get('user_id', '')
        db_data = AmbulanceRequestModel.get_ambulance_request(user_id=user_id, name=name)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'patient_id': each.patient,
                    'patient_name': each.name,
                    'email': each.email,
                    'phone_number': each.phone_number,
                    'gender': each.gender,
                    'image': '/static/' + each.image,
                    'source': each.source,
                    'destination': each.destination,
                    'description': each.description,
                    'user_type': each.user_type,
                    'status': each.status
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.ambulance_request_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)



@patient_bp.route('/add_ambulance_request_detail', methods=['POST'])
@Authentication.decode_auth_token
def add_ambulance_request_detail():
    try:
        driver = request.form['driver']
        ambulance_request = request.form['ambulance_request']
        ambulance = AmbulanceRequestDetailsModel(driver, ambulance_request)
        ambulance.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=ambulance.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@ambulance_bp.route('/update_ambulance_request_detail', methods=['POST'])
@Authentication.decode_auth_token
def update_ambulance_request_detail():
    try:
        id = request.form.get('id', "")
        ambulance_request_id = request.form.get('ambulance_request_id', "")
        data_to_update = {
            "status": request.form.get('status', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        AmbulanceRequestDetailsModel.update_by_id(id, data_to_update)
        if data_to_update['status'] == 'accepted':
            AmbulanceRequestModel.update_by_id(ambulance_request_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/get_ambulance_request_details', methods=['GET'])
@Authentication.decode_auth_token
def get_ambulance_request_details():
    try:
        driver = request.args.get('driver', '')
        id = request.args.get('id', '')
        patient = request.args.get('patient', '')
        ambulance_request_id = request.args.get('ambulance_request_id', '')
        db_data = AmbulanceRequestDetailsModel.get_ambulance_request(ambulance_request_id=ambulance_request_id, id=id,
                                                                     driver=driver, patient=patient)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'ambulance_id': each.driver,
                    'ambulance_name': each.ambulance_name,
                    'patient_id': each.patient,
                    'patient_name': each.patient_name,
                    'patient_number': each.patient_number,
                    'ambulance_number': each.ambulance_number,
                    'ambulance_request_id': each.ambulance_request,
                    'source': each.source,
                    'destination': each.destination,
                    'description': each.description,
                    'request_status': each.request_status,
                    'status': each.status
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.blood_request_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/delete_ambulance_request', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_ambulance_request():
    try:
        ambulance_request_id = request.args.get('ambulance_request_id', '')
        AmbulanceRequestModel.delete_by_id(ambulance_request_id)
        AmbulanceRequestDetailsModel.delete_by_ar_id(ambulance_request_id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)