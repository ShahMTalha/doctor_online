from . import db
import datetime
from .LabReportsModel import LabReportsModel
from .UserModel import UserModel
from sqlalchemy.orm import aliased


class PatientReportModel(db.Model):
    __tablename__ = 'patient_report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    lab = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    lab_report = db.Column(db.Integer, db.ForeignKey(LabReportsModel.id), nullable=False)
    report = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, patient, lab, lab_report, report):
        self.patient = patient
        self.lab = lab
        self.lab_report = lab_report
        self.report = report
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_patient_reports(patient_id="", id="", lab_id="", report_id=""):
        Patient = aliased(UserModel)
        Lab = aliased(UserModel)
        lab = PatientReportModel.query.with_entities(PatientReportModel.id, PatientReportModel.patient,
                                                     PatientReportModel.lab,
                                                     PatientReportModel.lab_report, LabReportsModel.price,
                                                     LabReportsModel.report_name,
                                                     Patient.name.label("patient_name"),
                                                     Lab.name.label("label_name")) \
            .join(Patient, PatientReportModel.patient == Patient.id) \
            .join(Lab, PatientReportModel.lab == Lab.id) \
            .join(LabReportsModel, PatientReportModel.lab_report == LabReportsModel.id)

        if patient_id:
            lab = lab.filter(PatientReportModel.patient == patient_id)
        if lab_id:
            lab = lab.filter(PatientReportModel.lab == lab_id)
        if id:
            lab = lab.filter(PatientReportModel.id == id)
        if report_id:
            lab = lab.filter(PatientReportModel.lab_report == report_id)

        lab = lab.all()
        return lab

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_user_id(patient_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        PatientReportModel.query.filter(PatientReportModel.patient == patient_id).update(updated_data)
        db.session.commit()