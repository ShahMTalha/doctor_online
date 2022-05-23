from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import ambulance_bp
from src.models.UserModel import UserModel
from src.models.AmbulanceDetailModel import AmbulanceDetailModel
from src.models.AmbulanceTypeModel import AmbulanceTypeModel
from src.common.FileHelper import FileHelper


@ambulance_bp.route('/add_details', methods=['POST'])
@Authentication.decode_auth_token
def add_details():
    try:
        user_id = request.form['user_id']
        address = request.form['address']
        own_by = request.form['own_by']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if UserModel.get_user(user_id=user_id, user_type='ambulance'):
            lab = AmbulanceDetailModel(user_id, address, own_by, latitude, longitude)
            lab.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                        data=lab.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@ambulance_bp.route('/update_detail', methods=['POST'])
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
        AmbulanceDetailModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@ambulance_bp.route('/get_details', methods=['GET'])
@Authentication.decode_auth_token
def get_details():
    try:
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        verified = request.args.get('verified', '')
        db_data = AmbulanceDetailModel.get_ambulance(user_id=user_id, name=name, verified=verified)

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


@ambulance_bp.route('/add_ambulance', methods=['POST'])
@Authentication.decode_auth_token
def add_ambulance():
    try:
        ambulance_detail_id = request.form['ambulance_detail_id']
        ambulance_type = request.form['ambulance_type']
        specification = request.form['specification']
        image = request.files.getlist("image[]")
        image_path = ""
        count = 1
        for each in image:
            file_name = ambulance_type.replace(' ', '_') + '_' + str(ambulance_detail_id) + '_' + str(count)
            image_path += FileHelper.upload_file('ambulance/' + file_name, each) + ' | '
            count += 1
        report = AmbulanceTypeModel(ambulance_detail_id, ambulance_type, specification, image_path)
        report.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                    data=report.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@ambulance_bp.route('/update_ambulance', methods=['POST'])
@Authentication.decode_auth_token
def update_ambulance():
    try:
        id = request.form.get('id', "")
        ambulance_detail_id = request.form['ambulance_detail_id']
        data_to_update = {
            "ambulance_type": request.form.get('ambulance_type', ""),
            "specification": request.form.get('specification', "")
        }
        image = request.files.getlist("image[]")
        image_path = ""
        if image:
            count = 1
            for each in image:
                file_name = data_to_update['ambulance_type'].replace(' ', '_') + '_' + str(ambulance_detail_id) + '_' + str(count)
                image_path += FileHelper.upload_file('ambulance/' + file_name, each) + ' | '
                count += 1
            data_to_update['image'] = image_path
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        AmbulanceTypeModel.update_by_id(id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@ambulance_bp.route('/delete_ambulance', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_ambulance():
    try:
        id = request.form.get('id', "")
        AmbulanceTypeModel.delete_by_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@ambulance_bp.route('/get_ambulance', methods=['GET'])
@Authentication.decode_auth_token
def get_ambulance():
    try:
        id = request.args.get('id', '')
        ambulance_detail_id = request.args.get('ambulance_detail_id', '')
        user_id = request.args.get('user_id', '')
        db_data = AmbulanceTypeModel.get_ambulance_types(id=id, ambulance_detail_id=ambulance_detail_id, user_id=user_id)
        if db_data:
            data = []
            for each in db_data:
                files = each.ambulance_type_image.split(' | ')
                final_files = []
                for each_file in files:
                    if each_file:
                        final_files.append('/static/' + each_file)
                each_rec = {
                    'id': each.id,
                    'ambulance_detail_id': each.ambulance_detail_id,
                    'ambulance_type': each.ambulance_type,
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
                    'image': '/static/' + each.image,
                    'ambulance_type_image':  final_files,
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.ambulance_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)
