from . import db
import datetime
from .UserModel import UserModel
from .AmbulanceRequestModel import AmbulanceRequestModel
from sqlalchemy.orm import aliased


class AmbulanceRequestDetailsModel(db.Model):
    __tablename__ = 'ambulance_request_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    ambulance_request = db.Column(db.Integer, db.ForeignKey(AmbulanceRequestModel.id), nullable=False)
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, driver, ambulance_request):
        self.driver = driver
        self.ambulance_request = ambulance_request
        self.status = 'pending'
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_ambulance_request(driver="", ambulance_request_id="", patient="", id=""):
        Patient = aliased(UserModel)
        Ambulance = aliased(UserModel)
        ambulance = AmbulanceRequestDetailsModel.query.with_entities(AmbulanceRequestDetailsModel.id, AmbulanceRequestDetailsModel.driver,
                                                             AmbulanceRequestDetailsModel.ambulance_request,
                                                             AmbulanceRequestDetailsModel.status, AmbulanceRequestModel.patient,
                                                             AmbulanceRequestModel.source,
                                                             AmbulanceRequestModel.description,
                                                             AmbulanceRequestModel.destination,
                                                             AmbulanceRequestModel.status.label("request_status"),
                                                             Patient.phone_number.label("patient_number"),
                                                             Ambulance.phone_number.label("ambulance_number"),
                                                             Patient.name.label("patient_name"),
                                                             Ambulance.name.label("ambulance_name")) \
            .join(Ambulance, AmbulanceRequestDetailsModel.driver == Ambulance.id)\
            .join(AmbulanceRequestModel, AmbulanceRequestDetailsModel.ambulance_request == AmbulanceRequestModel.id) \
            .join(Patient, AmbulanceRequestModel.patient == Patient.id)
        if driver:
            ambulance = ambulance.filter(AmbulanceRequestDetailsModel.driver == driver)
        if id:
            ambulance = ambulance.filter(AmbulanceRequestDetailsModel.id == id)
        if ambulance_request_id:
            ambulance = ambulance.filter(AmbulanceRequestDetailsModel.id == ambulance_request_id)
        if patient:
            ambulance = ambulance.filter(AmbulanceRequestModel.patient == patient)

        ambulance = ambulance.all()
        return ambulance


    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        AmbulanceRequestDetailsModel.query.filter(AmbulanceRequestDetailsModel.id == id and
                                                  AmbulanceRequestDetailsModel.status == 'pending')\
            .update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_ar_id(ambulance_request_id):
        AmbulanceRequestDetailsModel.query.filter(AmbulanceRequestDetailsModel.ambulance_request == ambulance_request_id).delete()
        db.session.commit()
