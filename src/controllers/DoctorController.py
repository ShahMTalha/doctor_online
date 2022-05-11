from flask import request, jsonify
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import doctor_bp
from src.models.UserModel import UserModel
from src.models.DoctorDetailModel import DoctorDetailModel


@doctor_bp.route('/add_details', methods=['POST'])
@Authentication.decode_auth_token
def add_details():
    try:
        user_id = request.form['user_id']
        age = request.form['age']
        qualification = request.form['qualification']
        serving = request.form['serving']
        experience = request.form.get('experience', "1")
        specialized = request.form['specialized']
        serving_type = request.form.get('serving_type', "public")
        if UserModel.get_user(user_id=user_id, user_type='doctor'):
            doctor = DoctorDetailModel(user_id, age, qualification, serving, experience, specialized, serving_type)
            doctor.save()
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='detail_id',
                                        data=doctor.id)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@doctor_bp.route('/update_detail', methods=['POST'])
@Authentication.decode_auth_token
def update_detail():
    try:
        user_id = request.form.get('user_id', "")
        data_to_update = {
            "age": request.form.get('age', ""),
            "qualification": request.form.get('qualification', ""),
            "serving": request.form.get('serving',""),
            "experience": request.form.get('experience',""),
            "specialized": request.form.get('specialized',""),
            "serving_type": request.form.get('serving_type', ""),
            "verified": request.form.get('verified', ""),
        }
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        DoctorDetailModel.update_by_user_id(user_id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@doctor_bp.route('/get_doctor', methods=['GET'])
@Authentication.decode_auth_token
def get_doctor():
    try:
        user_id = request.args.get('user_id', '')
        name = request.args.get('name', '')
        specialized = request.args.get('specialized', '')
        serving_type = request.args.get('serving_type', '')
        serving = request.args.get('serving', '')
        doctors_data = DoctorDetailModel.get_doctor(user_id=user_id, name=name, specialized=specialized, serving=serving,
                                                serving_type=serving_type)

        if doctors_data:
            data = []
            for doc_data in doctors_data:
                each = {
                    'id': doc_data.id,
                    'user_id': doc_data.user_id,
                    'name': doc_data.name,
                    'email': doc_data.email,
                    'phone_number': doc_data.phone_number,
                    'gender': doc_data.gender,
                    'age': doc_data.age,
                    'serving': doc_data.serving,
                    'qualification': doc_data.qualification,
                    'experience': doc_data.experience,
                    'specialized': doc_data.specialized,
                    'serving_type': doc_data.serving_type,
                    'verified': doc_data.verified,
                    'user_type': doc_data.user_type,
                    'image': '/static/' + doc_data.image
                }
                data.append(each)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.doctor_not_found.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)
