from flask import request, jsonify
from src.common.FileHelper import FileHelper
from src.common.Response import Response, ResponseMessages, ResponseCodes
from src.common.Authentication import Authentication
from . import user_bp
from src.models.UserModel import UserModel


@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone']
        gender = request.form['gender']
        user_type = request.form['user_type']
        image = request.files['image']
        if not UserModel.get_user(email=email):
            file_name = name.replace(' ', '_') + '_' + user_type
            image_path = FileHelper.upload_file('user_images/' + file_name, image)
            password_hash = Authentication.hash_password(password)
            user = UserModel(email, password_hash, name, phone_number, gender, user_type, image_path)
            user.save()
            token = Authentication.encode_auth_token(user.id)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='token',
                                        data=token)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@user_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        user_data = UserModel.get_user(email=email)
        if user_data:
            hash_password = user_data.password
            if Authentication.compare_password(password, hash_password):
                token = Authentication.encode_auth_token(user_data.id)
                response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, key='token',
                                            data=token)
            else:
                response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.password_not_matched.value)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)
    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@user_bp.route('/update', methods=['POST'])
@Authentication.decode_auth_token
def update_user():
    try:
        id = request.form.get('id', "")
        data_to_update = {
            "name": request.form.get('name', ""),
            "email": request.form.get('email', ""),
            "phone_number": request.form.get('phone',""),
            "gender": request.form.get('gender', "")
        }
        image = request.files.get('image', "")
        user_data = UserModel.get_user(user_id=id)
        if image:
            FileHelper.upload_file(user_data.image, image, no_extension=False)
        data_to_update = dict([(k, v) for k, v in data_to_update.items() if len(v) > 0])
        UserModel.update_by_id(id, data_to_update)
        response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@user_bp.route('/update_password', methods=['POST'])
def update_password():
    try:
        email = request.form['email']
        password = request.form['password']

        user_data = UserModel.get_user(email=email)
        if user_data:
            password_hash = Authentication.hash_password(password)
            data_to_update = {
                "password": password_hash,
            }
            UserModel.update_by_id(user_data.id, data_to_update)
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@user_bp.route('/verify_password', methods=['POST'])
@Authentication.decode_auth_token
def verify_password():
    try:
        id = request.form['id']
        password = request.form['password']

        user_data = UserModel.get_user(user_id=id)
        if user_data:
            hash_password = user_data.password
            if Authentication.compare_password(password, hash_password):
                response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value)
            else:
                response = Response.error(ResponseCodes.pre_condition.value,
                                          ResponseMessages.password_not_matched.value)
        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)


@user_bp.route('/get_user', methods=['GET'])
@Authentication.decode_auth_token
def get_user():
    try:
        id = request.args.get('id')
        user_data = UserModel.get_user(user_id=id)
        if user_data:
            data = {
                'id': user_data.id,
                'name': user_data.name,
                'email': user_data.email,
                'phone_number': user_data.phone_number,
                'gender': user_data.gender,
                'image': '/static/' + user_data.image
            }
            response = Response.success(ResponseCodes.success.value, ResponseMessages.success.value, data=data)

        else:
            response = Response.error(ResponseCodes.pre_condition.value, ResponseMessages.user_not_exists.value)

    except Exception as e:
        response = Response.error(ResponseCodes.forbidden.value, ResponseMessages.error.value + str(e))

    return jsonify(response)
