import enum


class ResponseCodes(enum.Enum):
    success = 200
    created = 201
    pre_condition = 401
    conflict = 403
    not_found = 404
    forbidden = 500


class ResponseMessages(enum.Enum):
    success = "Successfully completed/updated"
    error = "Something might went wrong: "
    user_exists = "Sign up failed user email already exists"
    password_not_matched = "You have entered a wrong password"
    user_not_exists = "Your requested user does not exists"
    medicine_exists = "Your requested medicine already exists"
    token_missing = "Valid token is missing"
    signature_expired = "Signature expired. Please log in again."
    invalid_token = "Invalid token. Please log in again."
    medicine_not_found = "No medicine found against search"
    doctor_not_found = "No doctor found against search"
    lab_not_found = "No lab found against search"
    store_not_found = "No medical store found against search"
    patient_not_found = "No user found against search"
    ambulance_not_found = "No ambulance found against search"
    blood_request_not_found = "No blood request found against search"
    ambulance_request_not_found = "No ambulance request found against search"
    precp_not_found = "No precreption found against search"
    appointment_not_found = "Appointment can not arranged slot not available or already taken"


class Response:
    @staticmethod
    def success(code, message, key='data', data={}):
        return {
            'code': code,
            'status': 'success',
            'message': message,
            key: data
        }

    @staticmethod
    def error(code, message):
        return {
            'code': code,
            'error-status': 'error',
            'error-message': message,
        }
