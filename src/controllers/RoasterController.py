from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import common_bp
from src.models.UserModel import UserModel
from src.models.RoasterModel import RoasterModel


@common_bp.route('/add_roaster', methods=['POST'])
@Authentication.decode_auth_token
def add_roaster():
    try:
        user_id = request.form['user_id']
        days = request.form['days']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        if UserModel.get_user(user_id=user_id):
            roaster = RoasterModel(user_id, days, start_time, end_time)
            roaster.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='roaster_id',
                                        data=roaster.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@common_bp.route('/update_roaster', methods=['POST'])
@Authentication.decode_auth_token
def update_roaster():
    try:
        user_id = request.form.get('user_id', "")
        data_to_update = {
            "days": request.form.get('days', ""),
            "start_time": request.form.get('start_time', ""),
            "end_time": request.form.get('end_time', ""),
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        RoasterModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@common_bp.route('/get_roaster', methods=['GET'])
@Authentication.decode_auth_token
def get_roaster():
    try:
        user_id = request.args.get('user_id')
        roaster_data = RoasterModel.get_roaster(user_id)
        if roaster_data:
            data = {
                'id': roaster_data.id,
                'user_id': roaster_data.user_id,
                'days': roaster_data.days,
                'start_time': roaster_data.start_time.strftime("%H:%M"),
                'end_time': roaster_data.end_time.strftime("%H:%M"),
            }
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@common_bp.route('/delete_roaster', methods=['DELETE'])
@Authentication.decode_auth_token
def delete_roaster():
    try:
        user_id = request.args.get('user_id')
        RoasterModel.delete_by_user_id(user_id)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)
