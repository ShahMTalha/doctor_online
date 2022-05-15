from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import patient_bp

from src.models.CartModel import CartModel
from src.models.OrderModel import OrderModel
from src.models.OrderDetailModel import OrderDetailModel
import json


@patient_bp.route('/get_cart', methods=['GET'])
@Authentication.decode_auth_token
def get_cart():
    try:
        user_id = request.args.get('user_id', '')
        id = request.args.get('id', '')
        store_medicine_id = request.args.get('store_medicine_id', '')
        db_data = CartModel.get_cart(user_id=user_id, id=id, store_medicine_id=store_medicine_id)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'patient_id': each.patient_id,
                    'medicine_id': each.medicine_id,
                    'quantity': each.quantity,
                    'store_id': each.store_id,
                    'price': each.price,
                    'patient_name': each.patient_name,
                    'store_name': each.store_name,
                    'name': each.name,
                    'image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.patient_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/add_cart', methods=['POST'])
@Authentication.decode_auth_token
def add_cart():
    try:
        patient_id = request.form['patient_id']
        store_id = request.form['store_id']
        store_medicine_id = request.form['store_medicine_id']
        quantity = request.form['quantity']
        cart = CartModel(patient_id, store_id, store_medicine_id, quantity)
        cart.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='cart_id',
                                    data=cart.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/update_cart', methods=['POST'])
@Authentication.decode_auth_token
def update_cart():
    try:
        id = request.form.get('id', "")
        data_to_update = {
            "quantity": request.form.get('quantity', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        CartModel.update_by_id(id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/delete_cart', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_cart():
    try:
        cart_id = request.form.get('cart_id', "")
        patient_id = request.form.get('patient_id', "")
        CartModel.delete_by_id(cart_id, patient_id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/get_order', methods=['GET'])
@Authentication.decode_auth_token
def get_order():
    try:
        id = request.args.get('id', '')
        user_id = request.args.get('user_id', '')
        store_id = request.args.get('store_id', '')
        db_data = OrderModel.get_order(user_id=user_id, id=id, store_id=store_id)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'patient_id': each.patient_id,
                    'total': each.total,
                    'status': each.status,
                    'store_id': each.store_id,
                    'patient_name': each.patient_name,
                    'store_name': each.store_name,
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.blood_request_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)



@patient_bp.route('/add_order', methods=['POST'])
@Authentication.decode_auth_token
def add_order():
    try:
        patient_id = request.form['patient_id']
        store_id = request.form['store_id']
        total = request.form['total']
        medicine_details = json.loads(request.form.get('medicine_details', "[]"))
        order = OrderModel(patient_id, store_id, total)
        order.save()
        if order:
            for each in medicine_details:
                order_detail = OrderDetailModel(order.id, each['store_medicine_id'], each['quantity'])
                order_detail.save()
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='order_id',
                                    data=order.id)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/update_order', methods=['POST'])
@Authentication.decode_auth_token
def update_order():
    try:
        order_id = request.form.get('order_id', "")
        data_to_update = {
            "status": request.form.get('status', "")
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        OrderModel.update_by_id(order_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))
    return jsonify(response)


@patient_bp.route('/get_order_details', methods=['GET'])
@Authentication.decode_auth_token
def get_order_details():
    try:
        id = request.args.get('id', '')
        user_id = request.args.get('user_id', '')
        store_id = request.args.get('store_id', '')
        db_data = OrderDetailModel.get_order(user_id=user_id, id=id, store_id=store_id)

        if db_data:
            data = []
            for each in db_data:
                each_rec = {
                    'id': each.id,
                    'order_id': each.order_id,
                    'quantity': each.quantity,
                    'patient_id': each.patient_id,
                    'store_id': each.store_id,
                    'total': each.total,
                    'status': each.status,
                    'patient_name': each.patient_name,
                    'store_name': each.store_name,
                    'medicine_id': each.medicine_id,
                    'price': each.price,
                    'med_name': each.med_name,
                    'image': '/static/' + each.image
                }
                data.append(each_rec)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.blood_request_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@patient_bp.route('/delete_order', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_order():
    try:
        id = request.args.get('id', '')
        OrderModel.delete_by_id(id)
        OrderDetailModel.delete_by_id(id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)