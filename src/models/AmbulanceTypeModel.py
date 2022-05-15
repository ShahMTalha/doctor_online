from . import db
import datetime
from .AmbulanceDetailModel import AmbulanceDetailModel
from .UserModel import UserModel


class AmbulanceTypeModel(db.Model):
    __tablename__ = 'ambulance_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ambulance_detail_id = db.Column(db.Integer, db.ForeignKey(AmbulanceDetailModel.id), nullable=False)
    ambulance_type = db.Column(db.String(), nullable=False)
    specification = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, ambulance_detail_id, ambulance_type, specification, image):
        self.ambulance_detail_id = ambulance_detail_id
        self.ambulance_type = ambulance_type
        self.specification = specification
        self.image = image
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_ambulance_types(user_id="", id="", ambulance_detail_id=""):
        ambulance = AmbulanceTypeModel.query.with_entities(AmbulanceTypeModel.id, AmbulanceTypeModel.ambulance_detail_id,
                                                           AmbulanceTypeModel.ambulance_type,
                                                           AmbulanceTypeModel.image.label("ambulance_type_image"),
                                                           AmbulanceTypeModel.specification, AmbulanceDetailModel.user_id,
                                                           AmbulanceDetailModel.address, AmbulanceDetailModel.latitude,
                                                           AmbulanceDetailModel.longitude, UserModel.name, UserModel.email,
                                                           UserModel.user_type, UserModel.phone_number, UserModel.gender,
                                                           UserModel.image, AmbulanceDetailModel.own_by,
                                                           AmbulanceDetailModel.verified) \
                        .join(AmbulanceDetailModel, AmbulanceTypeModel.ambulance_detail_id == AmbulanceDetailModel.id)\
                        .join(UserModel, AmbulanceDetailModel.user_id == UserModel.id)\
                        .filter(UserModel.user_type == 'ambulance')
        if user_id:
            ambulance = ambulance.filter(AmbulanceDetailModel.user_id == user_id)
        if id:
            ambulance = ambulance.filter(AmbulanceTypeModel.id == id)
        if ambulance_detail_id:
            ambulance = ambulance.filter(AmbulanceTypeModel.ambulance_detail_id == ambulance_detail_id)

        ambulance = ambulance.all()
        return ambulance

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        AmbulanceTypeModel.query.filter(AmbulanceTypeModel.id == id).update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(id):
        AmbulanceTypeModel.query.filter(AmbulanceTypeModel.id == id).delete()
        db.session.commit()