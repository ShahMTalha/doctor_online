from . import db
import datetime
from .UserModel import UserModel
from .LabReportsModel import LabReportsModel
from sqlalchemy.orm import aliased
from sqlalchemy import func


class AppointmentModel(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    appointer = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    date = db.Column(db.Date, nullable=False)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String())
    lab_report_id = db.Column(db.Integer, db.ForeignKey(LabReportsModel.id))
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, requester, appointer, date, day, start_time, end_time, address, lab_report_id):
        self.requester = requester
        self.appointer = appointer
        self.date = date
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.status = 'pending'
        self.address = address
        self.lab_report_id = lab_report_id
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        AppointmentModel.query.filter(AppointmentModel.id == id).update(updated_data)
        db.session.commit()

    @staticmethod
    def get_appointment(id="", requester="", appointer="", date="", day="", status=""):
        User_Requestor = aliased(UserModel)
        User_Appointer = aliased(UserModel)
        appointment = AppointmentModel.query.with_entities(AppointmentModel.id, AppointmentModel.requester,
                                                           AppointmentModel.appointer, AppointmentModel.date,
                                                           AppointmentModel.day, AppointmentModel.start_time,
                                                           AppointmentModel.end_time,
                                                           User_Appointer.name.label("appointer_name"),
                                                           User_Requestor.name.label("requestor_name"),
                                                           AppointmentModel.address, AppointmentModel.lab_report_id,
                                                           LabReportsModel.report_name, LabReportsModel.price,
                                                           AppointmentModel.status) \
        .join(User_Requestor, User_Requestor.id == AppointmentModel.requester) \
        .join(User_Appointer, User_Appointer.id == AppointmentModel.appointer) \
        .join(LabReportsModel, AppointmentModel.lab_report_id == LabReportsModel.id, isouter=True)
        if requester or appointer:
            if requester:
                appointment = appointment.filter(AppointmentModel.requester == requester)
            if appointer:
                appointment = appointment.filter(AppointmentModel.appointer == appointer)
            if id:
                appointment = appointment.filter(AppointmentModel.id != id)
        elif id:
            appointment = appointment.filter(AppointmentModel.id == id)
        if day:
            search = "%{}%".format(day.lower())
            appointment = appointment.filter(func.lower(AppointmentModel.day).like(search))
        if date:
            appointment = appointment.filter(AppointmentModel.date == date)
        if status:
            appointment = appointment.filter(func.lower(AppointmentModel.status) == status)

        appointment = appointment.all()
        return appointment

    @staticmethod
    def delete_by_id(id):
        AppointmentModel.query.filter(AppointmentModel.id == id).delete()
        db.session.commit()