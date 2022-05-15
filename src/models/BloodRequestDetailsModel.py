from . import db
import datetime
from .UserModel import UserModel
from .PatientDetailModel import PatientDetailModel
from .BloodRequestModel import BloodRequestModel
from sqlalchemy.orm import aliased


class BloodRequestDetailsModel(db.Model):
    __tablename__ = 'blood_request_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    blood_request = db.Column(db.Integer, db.ForeignKey(BloodRequestModel.id), nullable=False)
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, donor, blood_request):
        self.donor = donor
        self.blood_request = blood_request
        self.status = 'pending'
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_blood_request(donor="", blood_request_id="", patient="", id=""):
        Patient = aliased(UserModel)
        Donor = aliased(UserModel)
        blood = BloodRequestDetailsModel.query.with_entities(BloodRequestDetailsModel.id, BloodRequestDetailsModel.donor,
                                                             BloodRequestDetailsModel.blood_request,
                                                             BloodRequestDetailsModel.status, BloodRequestModel.patient,
                                                             BloodRequestModel.blood_group.label("request_blood"),
                                                             BloodRequestModel.description,
                                                             PatientDetailModel.blood_group.label("donor_blood"),
                                                             BloodRequestModel.bottles, BloodRequestModel.location,
                                                             BloodRequestModel.status.label("request_status"),
                                                             Patient.phone_number.label("patient_number"),
                                                             Donor.phone_number.label("donor_number"),
                                                             Patient.name.label("patient_name"),
                                                             Donor.name.label("donor_name")) \
            .join(Donor, BloodRequestDetailsModel.donor == Donor.id)\
            .join(PatientDetailModel, PatientDetailModel.user_id == Donor.id)\
            .join(BloodRequestModel, BloodRequestDetailsModel.blood_request == BloodRequestModel.id) \
            .join(Patient, BloodRequestModel.patient == Patient.id)
        if donor:
            blood = blood.filter(BloodRequestDetailsModel.donor == donor)
        if id:
            blood = blood.filter(BloodRequestDetailsModel.id == id)
        if blood_request_id:
            blood = blood.filter(BloodRequestDetailsModel.id == blood_request_id)
        if patient:
            blood = blood.filter(BloodRequestModel.patient == patient)

        blood = blood.all()
        return blood


    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        BloodRequestDetailsModel.query.filter(BloodRequestDetailsModel.id == id and BloodRequestDetailsModel.status == 'pending')\
            .update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_br_id(blood_request_id):
        BloodRequestDetailsModel.query.filter(BloodRequestDetailsModel.blood_request == blood_request_id).delete()
        db.session.commit()
