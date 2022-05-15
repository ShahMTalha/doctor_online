from . import db
import datetime
from .UserModel import UserModel
from sqlalchemy import func


class BloodRequestModel(db.Model):
    __tablename__ = 'blood_request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    blood_group = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    bottles = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, patient, blood_group, location, bottles, description):
        self.patient = patient
        self.blood_group = blood_group
        self.location = location
        self.bottles = bottles
        self.description = description
        self.status = 'pending'
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_blood_request(user_id="", name=None):
        blood = BloodRequestModel.query.with_entities(BloodRequestModel.id, BloodRequestModel.patient, UserModel.name,
                                                UserModel.email, UserModel.user_type, BloodRequestModel.status,
                                                UserModel.phone_number, UserModel.gender, UserModel.image,
                                                BloodRequestModel.blood_group, BloodRequestModel.location,
                                                BloodRequestModel.bottles, BloodRequestModel.description) \
                        .join(UserModel, BloodRequestModel.patient == UserModel.id)
        if user_id:
            blood = blood.filter(BloodRequestModel.patient == user_id)
        if name:
            search = "%{}%".format(name.lower())
            blood = blood.filter(func.lower(UserModel.name).like(search))

        blood = blood.all()
        return blood


    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        BloodRequestModel.query.filter(BloodRequestModel.id == id and BloodRequestModel.status == 'pending')\
            .update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(id):
        BloodRequestModel.query.filter(BloodRequestModel.id == id and BloodRequestModel.status == 'pending')\
            .delete()
        db.session.commit()