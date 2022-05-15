from . import db
import datetime
from .UserModel import UserModel
from sqlalchemy import func, text
from src.common.globals import geo_range


class PatientDetailModel(db.Model):
    __tablename__ = 'patient_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    address = db.Column(db.String(), nullable=False)
    father_name = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    blood_group = db.Column(db.String(), nullable=False)
    donating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, address, father_name, latitude, longitude, blood_group, donating):
        self.user_id = user_id
        self.address = address
        self.father_name = father_name
        self.latitude = latitude
        self.longitude = longitude
        self.blood_group = blood_group
        self.donating = donating
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_patient(user_id="", name=None):
        patient = UserModel.query.with_entities(PatientDetailModel.id, PatientDetailModel.user_id, UserModel.name,
                                                UserModel.email, PatientDetailModel.address, UserModel.user_type,
                                                UserModel.phone_number, UserModel.gender, UserModel.image,
                                                PatientDetailModel.father_name, PatientDetailModel.latitude,
                                                PatientDetailModel.longitude, PatientDetailModel.donating,
                                                PatientDetailModel.blood_group) \
                        .join(PatientDetailModel, UserModel.id == PatientDetailModel.user_id, isouter=True)\
                        .filter(UserModel.user_type == 'patient')
        if user_id:
            patient = patient.filter(PatientDetailModel.user_id == user_id)
        if name:
            search = "%{}%".format(name.lower())
            patient = patient.filter(func.lower(UserModel.name).like(search))

        patient = patient.all()
        return patient

    @staticmethod
    def get_donating_patients(lat, long, offset, limit, own_id):
        query = text("SELECT pd.id, pd.latitude, pd.longitude, pd.user_id, u.name, u.email,  u.image,\
                 distance, pd.address, pd.blood_group, u.image \
                 FROM patient_detail pd inner join users u on pd.user_id = u.id CROSS JOIN LATERAL \
                (VALUES ( SQRT(POW(69.1 * (pd.latitude - " + str(lat) + "), 2) + POW(69.1 * (" + str(long) + " - pd.longitude) \
                * COS(pd.latitude / 57.3), 2)) )) v(distance) where v.distance < " + str(geo_range) + " and\
                 u.user_type = 'patient' and pd.donating = 1 and pd.user_id != " + str(own_id) + " \
                order by distance asc  limit " + str(limit) + " offset " + str(offset) + "")
        patient = db.engine.execute(query).all()
        return patient

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_user_id(user_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        PatientDetailModel.query.filter(PatientDetailModel.user_id == user_id).update(updated_data)
        db.session.commit()