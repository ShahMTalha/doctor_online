from functools import wraps
import bcrypt
from flask import request, jsonify
import jwt
import os
import datetime
from src.common.Response import ResponseCodes, ResponseMessages, Response
from src.common.globals import verify_token


class Authentication:

    @staticmethod
    def decode_auth_token(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                message = ''
                if verify_token:
                    token = None
                    if 'x-access-tokens' in request.headers:
                        token = request.headers['x-access-tokens']

                    if not token:
                        message = ResponseMessages.token_missing.value

                    payload = jwt.decode(
                        token,
                        os.getenv("SECRET_KEY", "this-is-the-default-key"),
                        algorithms='HS256'
                    )
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                message = ResponseMessages.signature_expired.value
            except jwt.InvalidTokenError:
                message = ResponseMessages.invalid_token.value

            if message:
                return jsonify(Response.error(ResponseCodes.conflict.value, message))

        return decorator

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=50),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv("SECRET_KEY", "this-is-the-default-key"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def hash_password(password):
        binary_password = password.encode('ascii')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(binary_password, salt)
        decode_hash = hashed.decode('ascii')
        return decode_hash

    @staticmethod
    def compare_password(password, hashed):
        matched = False
        binary_password = password.encode('ascii')
        binary_hash = hashed.encode('ascii')
        if bcrypt.checkpw(binary_password, binary_hash):
            matched = True
        return matched



