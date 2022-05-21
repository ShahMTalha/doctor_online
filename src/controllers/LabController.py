import datetime

from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import lab_bp
from src.models.UserModel import UserModel
from src.models.LabDetailModel import LabDetailModel
from src.models.LabReportsModel import LabReportsModel
from src.models.PatientReportModel import PatientReportModel
from src.models.PatientHistoryModel import PatientHistoryModel
from src.common.FileHelper import FileHelper


@lab_bp.route('/add_details', methods=['POST'])
@Authentication.decode_auth_token
def add_details():
    try:
        user_id = request.form['user_id']
        address = request.form['address']
        own_by = request.form['own_by']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if UserModel.get_user(user_id=user_id, user_type='lab'):
            lab = LabDetailModel(user_id, address, own_by, latitude, longitude)
            lab.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                        data=lab.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@lab_bp.route('/update_detail', methods=['POST'])
@Authentication.decode_auth_token
def update_detail():
    try:
        user_id = request.form.get('user_id', "")
        data_to_update = {
            "address": request.form.get('address', ""),
            "own_by": request.form.get('own_by', ""),
            "latitude": request.form.get('latitude', ""),
            "longitude": request.form.get('longitude', ""),
            "verified": request.form.get('verified', ""),
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        LabDetailModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@lab_bp.route('/get_lab_details', methods=['GET'])
@Authentication.decode_auth_token
def get_lab_details():
    try:
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        verified = request.args.get('verified', '')
        db_data = LabDetailModel.get_lab(user_id=user_id, name=name, verified=verified)

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
                    'own_by': each.own_by,
                    'latitude': each.latitude,
                    'longitude': each.longitude,
                    'verified': each.verified,
                    'user_type': each.user_type,
                    'image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.lab_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@lab_bp.route('/get_lab_by_location', methods=['GET'])
@Authentication.decode_auth_token
def get_lab_by_location():
    try:
        lat = request.args.get('lat', '')
        long = request.args.get('long', '')
        offset = request.args.get('offset', '')
        limit = request.args.get('limit', '')
        own_id = request.args.get('own_id', '')
        db_data = LabDetailModel.get_lab_by_location(lat, long, offset, limit, own_id)

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


@lab_bp.route('/add_reports', methods=['POST'])
@Authentication.decode_auth_token
def add_reports():
    try:
        lab_detail_id = request.form['lab_detail_id']
        report_name = request.form['report_name']
        price = request.form['price']
        specification = request.form['specification']
        report = LabReportsModel(lab_detail_id, report_name, price, specification)
        report.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=report.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@lab_bp.route('/update_report', methods=['POST'])
@Authentication.decode_auth_token
def update_report():
    try:
        id = request.form.get('id', "")
        data_to_update = {
            "report_name": request.form.get('report_name', ""),
            "price": request.form.get('price', ""),
            "specification": request.form.get('specification', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        LabReportsModel.update_by_id(id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@lab_bp.route('/delete_report', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_report():
    try:
        id = request.form.get('id', "")
        LabReportsModel.delete_by_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@lab_bp.route('/get_report', methods=['GET'])
@Authentication.decode_auth_token
def get_report():
    try:
        id = request.args.get('id', '')
        lab_detail_id = request.args.get('lab_detail_id', '')
        user_id = request.args.get('user_id', '')
        db_data = LabReportsModel.get_lab_reports(id=id, lab_detail_id=lab_detail_id, user_id=user_id)
        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'lab_detail_id': each.lab_detail_id,
                    'report_name': each.report_name,
                    'price': each.price,
                    'specification': each.specification,
                    'user_id': each.user_id,
                    'address': each.address,
                    'latitude': each.latitude,
                    'name': each.name,
                    'email': each.email,
                    'phone_number': each.phone_number,
                    'gender': each.gender,
                    'own_by': each.own_by,
                    'longitude': each.longitude,
                    'user_type': each.user_type,
                    'verified': each.verified,
                    'image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.lab_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)

@lab_bp.route('/add_patient_report', methods=['POST'])
@Authentication.decode_auth_token
def add_patient_report():
    try:
        patient = request.form['patient']
        lab = request.form['lab']
        lab_report_id = request.form['lab_report']
        file = request.files['report']
        file_name = patient.replace(' ', '_') + '_' + lab + '_' + datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        file_path = FileHelper.upload_file('patient_reports/' + file_name, file)
        report = PatientReportModel(patient, lab, lab_report_id, file_path)
        report.save()
        history = PatientHistoryModel(patient, patient_report=str(report.id))
        history.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=report.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)