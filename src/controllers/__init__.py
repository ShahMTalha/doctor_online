from flask import Blueprint

user_bp = Blueprint('users', __name__)
doctor_bp = Blueprint('doctors', __name__)
patient_bp = Blueprint('patient', __name__)
lab_bp = Blueprint('lab', __name__)
store_bp = Blueprint('store', __name__)
ambulance_bp = Blueprint('ambulance_bp', __name__)
common_bp = Blueprint('common', __name__)



@user_bp.route('/')
def index():
    return "Welcome to user"


from src.controllers import UserController, DoctorController, RoasterController, AppointmentController, \
    MedicineController, LabController, AmbulanceController, StoreController, AmbulanceRequestController, \
    BloodRequestController, OrderController, PatientController
