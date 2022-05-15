from . import db
import datetime
from .UserModel import UserModel
from sqlalchemy import func


class AmbulanceRequestModel(db.Model):
    __tablename__ = 'ambulance_request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    source = db.Column(db.String(), nullable=False)
    destination = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, patient, source, destination, description):
        self.patient = patient
        self.description = description
        self.source = source
        self.destination = destination
        self.status = 'pending'
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_ambulance_request(user_id="", name=None):
        ambulance = AmbulanceRequestModel.query.with_entities(AmbulanceRequestModel.id, AmbulanceRequestModel.patient, UserModel.name,
                                                UserModel.email, UserModel.user_type, AmbulanceRequestModel.status,
                                                UserModel.phone_number, UserModel.gender, UserModel.image,
                                                AmbulanceRequestModel.source, AmbulanceRequestModel.destination,
                                                AmbulanceRequestModel.status, AmbulanceRequestModel.description) \
                        .join(UserModel, AmbulanceRequestModel.patient == UserModel.id)
        if user_id:
            ambulance = ambulance.filter(AmbulanceRequestModel.patient == user_id)
        if name:
            search = "%{}%".format(name.lower())
            ambulance = ambulance.filter(func.lower(UserModel.name).like(search))

        ambulance = ambulance.all()
        return ambulance


    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        AmbulanceRequestModel.query.filter(AmbulanceRequestModel.id == id and AmbulanceRequestModel.status == 'pending')\
            .update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(id):
        AmbulanceRequestModel.query.filter(AmbulanceRequestModel.id == id and AmbulanceRequestModel.status == 'pending')\
            .delete()
        db.session.commit()