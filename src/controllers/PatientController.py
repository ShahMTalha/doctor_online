import datetime

from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import patient_bp
from src.models.UserModel import UserModel
from src.models.PatientDetailModel import PatientDetailModel
from src.models.PatientHistoryModel import PatientHistoryModel
from src.common.FileHelper import FileHelper


@patient_bp.route('/add_details', methods=['POST'])
@Authentication.decode_auth_token
def add_details():
    try:
        user_id = request.form['user_id']
        address = request.form['address']
        father_name = request.form['father_name']
        blood_group = request.form['blood_group']
        donating = request.form['donating']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if UserModel.get_user(user_id=user_id, user_type='patient'):
            patient = PatientDetailModel(user_id, address, father_name, latitude, longitude, blood_group, donating)
            patient.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                        data=patient.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/update_detail', methods=['POST'])
@Authentication.decode_auth_token
def update_detail():
    try:
        user_id = request.form.get('user_id', "")
        data_to_update = {
            "address": request.form.get('address', ""),
            "father_name": request.form.get('father_name', ""),
            "blood_group": request.form.get('blood_group', ""),
            "latitude": request.form.get('latitude', ""),
            "longitude": request.form.get('longitude', ""),
            "donating": request.form.get('donating', ""),
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        PatientDetailModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/get_details', methods=['GET'])
@Authentication.decode_auth_token
def get_details():
    try:
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        db_data = PatientDetailModel.get_patient(user_id=user_id, name=name)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'user_id': each.user_id,
                    'name': each.name,
                    'email': each.email,
                    'phone_number': each.phone_number,
                    'gender': each.gender,
                    'address': each.address,
                    'father_name': each.father_name,
                    'blood_group': each.blood_group,
                    'latitude': each.latitude,
                    'longitude': each.longitude,
                    'donating': each.donating,
                    'user_type': each.user_type,
                    'image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.patient_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/add_history', methods=['POST'])
@Authentication.decode_auth_token
def add_history():
    try:
        patient = request.form['patient']
        title = request.form['title']
        detail = request.form['detail']
        file = request.files['file']
        file_name = patient.replace(' ', '_') + '_' + datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        file_path = FileHelper.upload_file('patient_reports/' + file_name, file)
        history = PatientHistoryModel(patient, title=title, detail=detail, file=file_path)
        history.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=history.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/delete_history', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_history():
    try:
        id = request.form.get('id', "")
        PatientHistoryModel.delete_by_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/get_history', methods=['GET'])
@Authentication.decode_auth_token
def get_history():
    try:
        id = request.args.get('id', '')
        user_id = request.args.get('user_id', '')
        db_data = PatientHistoryModel.get_patient_history(id=id, patient_id=user_id)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'patient_id': each.patient,
                    'patient_name': each.patient_name,
                    'doctor_id': each.doctor,
                    'doctor_name': each.doctor_name,
                    'title': each.title,
                    'detail': each.detail,
                    'file': '/static/' + each.file if each.file else '',
                    'patient_report_id': each.patient_report,
                    'report_name': each.report_name,
                    'report': '/static/' + each.report if each.report else '',
                    'lab_report_id': each.lab_report_id,
                    'lab_name': each.lab_name,
                    'precreption_id': each.precreption,
                    'notes': each.notes,
                    'severity': each.severity,
                    'status': each.status
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.patient_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)

