from . import db
import datetime
from .PrecreptionModel import PrecreptionModel
from .UserModel import UserModel
from .MedicineModel import MedicineModel
from sqlalchemy.orm import aliased


class PrecreptionDetailModel(db.Model):
    __tablename__ = 'precreption_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    precp_id = db.Column(db.Integer, db.ForeignKey(PrecreptionModel.id), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey(MedicineModel.id), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.String(), nullable=False)
    amount = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, precp_id, medicine_id, days, frequency, amount):
        self.precp_id = precp_id
        self.medicine_id = medicine_id
        self.days = days
        self.frequency = frequency
        self.amount = amount
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def get_precreption(id="", doctor="", patient=""):
        DoctorTab = aliased(UserModel)
        PatientTab = aliased(UserModel)
        precreption = PrecreptionModel.query.with_entities(PrecreptionModel.id, PrecreptionModel.doctor,
                                                           PrecreptionModel.patient, PrecreptionModel.notes,
                                                           PrecreptionModel.severity, PrecreptionModel.status,
                                                           PrecreptionDetailModel.medicine_id,
                                                           PrecreptionDetailModel.amount,
                                                           PrecreptionDetailModel.frequency,
                                                           PrecreptionDetailModel.days,
                                                           MedicineModel.name, MedicineModel.company,
                                                           MedicineModel.image,
                                                           DoctorTab.name.label("doctor_name"),
                                                           PatientTab.name.label("patient_name")) \
            .join(DoctorTab, PrecreptionModel.doctor == DoctorTab.id) \
            .join(PatientTab, PrecreptionModel.patient == PatientTab.id) \
            .join(PrecreptionDetailModel, PrecreptionDetailModel.precp_id == PrecreptionModel.id, isouter=True) \
            .join(MedicineModel, PrecreptionDetailModel.medicine_id == MedicineModel.id, isouter=True)
        if id:
            precreption = precreption.filter(PrecreptionModel.id == id)
        if doctor:
            precreption = precreption.filter(PrecreptionModel.doctor == doctor)
        if patient:
            precreption = precreption.filter(PrecreptionModel.patient == patient)

        precreption = precreption.all()
        return precreption

