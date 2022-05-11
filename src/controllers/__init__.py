from flask import Blueprint

user_bp = Blueprint('users', __name__)
doctor_bp = Blueprint('doctors', __name__)
common_bp = Blueprint('common', __name__)



@user_bp.route('/')
def index():
    return "Welcome to user"


from src.controllers import UserController, DoctorController, RoasterController, AppointmentController, MedicineController
