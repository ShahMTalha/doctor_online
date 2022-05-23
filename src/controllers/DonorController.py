from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import donor_bp
from src.models.UserModel import UserModel
from src.models.BloodDonorDetailModel import BloodDonorDetailModel


@donor_bp.route('/add_details', methods=['POST'])
@Authentication.decode_auth_token
def add_details():
    try:
        user_id = request.form['user_id']
        address = request.form['address']
        blood_group = request.form['blood_group']
        donating = request.form['donating']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if UserModel.get_user(user_id=user_id, user_type='donor'):
            donor = BloodDonorDetailModel(user_id, address, latitude, longitude, blood_group, donating)
            donor.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                        data=donor.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@donor_bp.route('/update_detail', methods=['POST'])
@Authentication.decode_auth_token
def update_detail():
    try:
        user_id = request.form.get('user_id', "")
        data_to_update = {
            "address": request.form.get('address', ""),
            "blood_group": request.form.get('blood_group', ""),
            "latitude": request.form.get('latitude', ""),
            "longitude": request.form.get('longitude', ""),
            "donating": request.form.get('donating', ""),
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        BloodDonorDetailModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@donor_bp.route('/get_details', methods=['GET'])
@Authentication.decode_auth_token
def get_details():
    try:
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        db_data = BloodDonorDetailModel.get_patient(user_id=user_id, name=name)

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
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.donor_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@donor_bp.route('/get_donors_nearby', methods=['GET'])
@Authentication.decode_auth_token
def get_donors_nearby():
    try:
        lat = request.args.get('lat', '')
        long = request.args.get('long', '')
        offset = request.args.get('offset', '')
        limit = request.args.get('limit', '')
        own_id = request.args.get('own_id', '')
        db_data = BloodDonorDetailModel.get_donors_nearby(lat, long, offset, limit, own_id)
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
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.donor_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)




