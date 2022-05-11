from . import db
import datetime
from .UserModel import UserModel
from sqlalchemy import func


class DoctorDetailModel(db.Model):
    __tablename__ = 'doctor_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    qualification = db.Column(db.String(), nullable=False)
    serving = db.Column(db.String(), nullable=False)
    experience = db.Column(db.Integer)
    specialized = db.Column(db.String(), nullable=False)
    serving_type = db.Column(db.String(10), nullable=False)
    verified = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, age, qualification, serving, experience, specialized, serving_type):
        self.user_id = user_id
        self.age = age
        self.qualification = qualification
        self.serving = serving
        self.experience = experience
        self.specialized = specialized
        self.serving_type = serving_type.lower()
        self.verified = 0
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_doctor(user_id="", name=None, specialized=None, serving_type=None, serving=None):
        doctor = UserModel.query.with_entities(DoctorDetailModel.id, DoctorDetailModel.user_id, UserModel.name,
                                               UserModel.email, DoctorDetailModel.specialized,
                                               UserModel.user_type, UserModel.phone_number, UserModel.gender,
                                               UserModel.image, DoctorDetailModel.age, DoctorDetailModel.serving,
                                               DoctorDetailModel.qualification, DoctorDetailModel.experience,
                                               DoctorDetailModel.serving_type, DoctorDetailModel.verified) \
                        .join(DoctorDetailModel, UserModel.id == DoctorDetailModel.user_id, isouter=True)\
                        .filter(UserModel.user_type == 'doctor')
        if user_id:
            doctor = doctor.filter(DoctorDetailModel.user_id == user_id)
        if name:
            search = "%{}%".format(name.lower())
            doctor = doctor.filter(func.lower(UserModel.name).like(search))
        if serving:
            search = "%{}%".format(serving.lower())
            doctor = doctor.filter(func.lower(DoctorDetailModel.serving).like(search))
        if specialized:
            search = "%{}%".format(specialized.lower())
            doctor = doctor.filter(func.lower(DoctorDetailModel.specialized).like(search))
        if serving_type:
            doctor = doctor.filter(func.lower(DoctorDetailModel.serving_type) == serving_type.lower())

        doctor = doctor.all()
        return doctor

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_user_id(user_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        DoctorDetailModel.query.filter(DoctorDetailModel.user_id == user_id).update(updated_data)
        db.session.commit()