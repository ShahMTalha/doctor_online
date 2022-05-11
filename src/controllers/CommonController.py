from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import common_bp
from src.common.FileHelper import FileHelper
from src.models.UserModel import UserModel
from src.models.RoasterModel import RoasterModel
from src.models.MedicineModel import MedicineModel


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


@common_bp.route('/add_medicine', methods=['POST'])
@Authentication.decode_auth_token
def add_medicine():
    try:
        user_id = request.form['user_id']
        name = request.form['name']
        country = request.form['country']
        company = request.form['company']
        med_type = request.form['med_type']
        weight = request.form['weight']
        image = request.files['image']
        if UserModel.get_user(user_id=user_id):
            file_name = name.replace(' ', '_') + '_' + med_type
            image_path = FileHelper.upload_file('medicines/' + file_name, image)
            medicine = MedicineModel(user_id, name, company, med_type, weight, country, image_path)
            medicine.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='med_id',
                                        data=medicine.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@common_bp.route('/get_medicine', methods=['GET'])
@Authentication.decode_auth_token
def get_medicine():
    try:
        id = request.args.get('id', '')
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        med_type = request.args.get('med_type', '')
        company = request.args.get('company', '')
        medicine_data = MedicineModel.find_medicines(id=id, user_id=user_id, name=name, med_type=med_type,
                                                     company=company)

        if medicine_data:
            data = []
            for med_data in medicine_data:
                each = {
                    'id': med_data.id,
                    'user_id': med_data.user_id,
                    'name': med_data.name,
                    'company': med_data.company,
                    'med_type': med_data.med_type,
                    'weight': med_data.weight,
                    'country': med_data.country,
                    'image': '/static/' + med_data.image
                }
                data.append(each)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.medicine_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)
