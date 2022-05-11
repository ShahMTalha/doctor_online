from . import db
import datetime
from .UserModel import UserModel



class PrecreptionModel(db.Model):
    __tablename__ = 'precreption'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    patient = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    notes = db.Column(db.String(), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, doctor, patient, notes, severity):
        self.doctor = doctor
        self.patient = patient
        self.notes = notes
        self.severity = severity
        self.status = 'generated'
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)


