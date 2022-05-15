from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import store_bp
from src.models.UserModel import UserModel
from src.models.StoreDetailModel import StoreDetailModel
from src.models.StoreMedicinesModel import StoreMedicinesModel
from src.models.MedicineModel import MedicineModel


@store_bp.route('/add_details', methods=['POST'])
@Authentication.decode_auth_token
def add_details():
    try:
        user_id = request.form['user_id']
        address = request.form['address']
        own_by = request.form['own_by']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if UserModel.get_user(user_id=user_id, user_type='store'):
            store = StoreDetailModel(user_id, address, own_by, latitude, longitude)
            store.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                        data=store.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@store_bp.route('/update_detail', methods=['POST'])
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
        StoreDetailModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@store_bp.route('/get_details', methods=['GET'])
@Authentication.decode_auth_token
def get_details():
    try:
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        db_data = StoreDetailModel.get_store(user_id=user_id, name=name)

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
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.store_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@store_bp.route('/get_store_by_location', methods=['GET'])
@Authentication.decode_auth_token
def get_store_details():
    try:
        lat = request.args.get('lat', '')
        long = request.args.get('long', '')
        offset = request.args.get('offset', '')
        limit = request.args.get('limit', '')
        own_id = request.args.get('own_id', '')
        db_data = StoreDetailModel.get_store_by_location(lat, long, offset, limit, own_id)

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
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.store_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@store_bp.route('/add_store_medicines', methods=['POST'])
@Authentication.decode_auth_token
def add_store_medicines():
    try:
        store_detail_id = request.form['store_detail_id']
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        price = request.form['price']
        description = request.form['description']
        if not MedicineModel.find_medicines(id=medicine_id):
            store_med = StoreMedicinesModel(store_detail_id, medicine_id, quantity, price, description)
            store_med.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='store_med_id',
                                        data=store_med.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.medicine_exists.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@store_bp.route('/update_store_medicines', methods=['POST'])
@Authentication.decode_auth_token
def update_store_medicines():
    try:
        id = request.form.get('id', "")
        data_to_update = {
            "price": request.form.get('price', ""),
            "quantity": request.form.get('quantity', ""),
            "description": request.form.get('description', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        StoreMedicinesModel.update_by_id(id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@store_bp.route('/delete_store_medicines', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_store_medicines():
    try:
        id = request.form.get('id', "")
        StoreMedicinesModel.delete_by_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@store_bp.route('/get_store_medicines', methods=['GET'])
@Authentication.decode_auth_token
def get_store_medicines():
    try:
        id = request.args.get('id', '')
        store_detail_id = request.args.get('store_detail_id', '')
        user_id = request.args.get('user_id', '')
        db_data = StoreMedicinesModel.get_store_medicines(id=id, store_detail_id=store_detail_id, user_id=user_id)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'store_detail_id': each.store_detail_id,
                    'medicine_id': each.medicine_id,
                    'price': each.price,
                    'description': each.description,
                    'user_id': each.user_id,
                    'store_name': each.store_name,
                    'med_name': each.med_name,
                    'med_type': each.med_type,
                    'weight': each.weight,
                    'company': each.company,
                    'country': each.country,
                    'own_by': each.own_by,
                    'user_type': each.user_type,
                    'med_image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.store_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)
