from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import patient_bp

from src.models.PatientDetailModel import PatientDetailModel
from src.models.BloodRequestModel import BloodRequestModel
from src.models.BloodRequestDetailsModel import BloodRequestDetailsModel


@patient_bp.route('/get_donating_patients', methods=['GET'])
@Authentication.decode_auth_token
def get_donating_patients():
    try:
        lat = request.args.get('lat', '')
        long = request.args.get('long', '')
        offset = request.args.get('offset', '')
        limit = request.args.get('limit', '')
        own_id = request.args.get('own_id', '')
        db_data = PatientDetailModel.get_donating_patients(lat, long, offset, limit, own_id)
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
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.patient_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/add_blood_request', methods=['POST'])
@Authentication.decode_auth_token
def add_blood_request():
    try:
        patient = request.form['patient']
        blood_group = request.form['blood_group']
        location = request.form['location']
        bottles = request.form['bottles']
        description = request.form['description']
        blood = BloodRequestModel(patient, blood_group, location, bottles, description)
        blood.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=blood.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/update_blood_request', methods=['POST'])
@Authentication.decode_auth_token
def update_blood_request():
    try:
        blood_request_id = request.form.get('blood_request_id', "")
        data_to_update = {
            "blood_group": request.form.get('blood_group', ""),
            "location": request.form.get('location', ""),
            "bottles": request.form.get('bottles', ""),
            "description": request.form.get('description', ""),
            "status": request.form.get('status', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        BloodRequestModel.update_by_id(blood_request_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/get_blood_request', methods=['GET'])
@Authentication.decode_auth_token
def get_blood_request():
    try:
        name = request.args.get('name', '')
        user_id = request.args.get('user_id', '')
        db_data = BloodRequestModel.get_blood_request(user_id=user_id, name=name)

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
                    'blood_group': each.blood_group,
                    'location': each.location,
                    'bottles': each.bottles,
                    'description': each.description,
                    'user_type': each.user_type,
                    'status': each.status
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.blood_request_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)



@patient_bp.route('/add_blood_request_detail', methods=['POST'])
@Authentication.decode_auth_token
def add_blood_request_detail():
    try:
        donor = request.form['donor']
        blood_request = request.form['blood_request']
        blood = BloodRequestDetailsModel(donor, blood_request)
        blood.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=blood.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/update_blood_request_details', methods=['POST'])
@Authentication.decode_auth_token
def update_blood_request_details():
    try:
        id = request.form.get('id', "")
        blood_request_id = request.form.get('blood_request_id', "")
        data_to_update = {
            "status": request.form.get('status', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        BloodRequestDetailsModel.update_by_id(id, data_to_update)
        if data_to_update['status'] == 'accepted':
            BloodRequestModel.update_by_id(blood_request_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/get_blood_request_details', methods=['GET'])
@Authentication.decode_auth_token
def get_blood_request_details():
    try:
        donor = request.args.get('donor', '')
        id = request.args.get('id', '')
        patient = request.args.get('patient', '')
        blood_request_id = request.args.get('blood_request_id', '')
        db_data = BloodRequestDetailsModel.get_blood_request(blood_request_id=blood_request_id, id=id, donor=donor,
                                                             patient=patient)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'donor_id': each.donor,
                    'donor_name': each.patient_name,
                    'patient_id': each.patient,
                    'patient_name': each.patient_name,
                    'patient_number': each.patient_number,
                    'donor_number': each.donor_number,
                    'blood_request_id': each.blood_request,
                    'request_blood': each.request_blood,
                    'donor_blood': each.donor_blood,
                    'location': each.location,
                    'bottles': each.bottles,
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


@patient_bp.route('/delete_blood_request', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_blood_request():
    try:
        blood_request_id = request.args.get('blood_request_id', '')
        BloodRequestModel.delete_by_id(blood_request_id)
        BloodRequestDetailsModel.delete_by_br_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)