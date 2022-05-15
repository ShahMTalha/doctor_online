from . import db
import datetime
from .PatientReportModel import PatientReportModel
from .LabReportsModel import LabReportsModel
from .PrecreptionModel import PrecreptionModel
from .UserModel import UserModel
from sqlalchemy.orm import aliased


class PatientHistoryModel(db.Model):
    __tablename__ = 'patient_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    title = db.Column(db.String())
    detail = db.Column(db.String())
    file = db.Column(db.String())
    patient_report = db.Column(db.Integer, db.ForeignKey(PatientReportModel.id))
    precreption = db.Column(db.Integer, db.ForeignKey(PrecreptionModel.id))
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, patient, title=None, detail=None, file=None, patient_report=None, precreption=None):
        self.patient = patient
        self.title = title
        self.detail = detail
        self.file = file
        self.patient_report = patient_report
        self.precreption = precreption
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_patient_history(patient_id="", id=""):
        Patient = aliased(UserModel)
        Lab = aliased(UserModel)
        Doctor = aliased(UserModel)
        history = PatientHistoryModel.query.with_entities(PatientHistoryModel.id, PatientHistoryModel.patient,
                                                          PatientHistoryModel.title,
                                                          PatientHistoryModel.detail, PatientHistoryModel.file,
                                                          PatientHistoryModel.patient_report, PatientHistoryModel.precreption,
                                                          PatientReportModel.report, LabReportsModel.report_name,
                                                          LabReportsModel.id.label("lab_report_id"),
                                                          PrecreptionModel.doctor,
                                                          PrecreptionModel.notes,
                                                          PrecreptionModel.severity,
                                                          PrecreptionModel.status,
                                                          Patient.name.label("patient_name"),
                                                          Lab.name.label("lab_name"),
                                                          Doctor.name.label("doctor_name")) \
            .join(Patient, PatientHistoryModel.patient == Patient.id) \
            .join(PatientReportModel, PatientHistoryModel.patient_report == PatientReportModel.id, isouter=True) \
            .join(LabReportsModel, PatientReportModel.lab_report == LabReportsModel.id, isouter=True) \
            .join(Lab, PatientReportModel.lab == Lab.id, isouter=True) \
            .join(PrecreptionModel, PatientHistoryModel.precreption == PrecreptionModel.id, isouter=True) \
            .join(Doctor, PrecreptionModel.doctor == Doctor.id, isouter=True)

        if patient_id:
            history = history.filter(PatientHistoryModel.patient == patient_id)
        if id:
            history = history.filter(PatientHistoryModel.id == id)

        history = history.all()
        return history

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def delete_by_id(id):
        PatientHistoryModel.query.filter(PatientHistoryModel.id == id).delete()
        db.session.commit()