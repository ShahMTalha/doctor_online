from . import db
import datetime
from .LabDetailModel import LabDetailModel
from .UserModel import UserModel


class LabReportsModel(db.Model):
    __tablename__ = 'lab_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_detail_id = db.Column(db.Integer, db.ForeignKey(LabDetailModel.id), nullable=False)
    report_name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    specification = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, lab_detail_id, report_name, price, specification):
        self.lab_detail_id = lab_detail_id
        self.report_name = report_name
        self.price = price
        self.specification = specification
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_lab_reports(user_id="", id="", lab_detail_id=""):
        lab = LabReportsModel.query.with_entities(LabReportsModel.id, LabReportsModel.lab_detail_id,
                                                  LabReportsModel.report_name, LabReportsModel.price,
                                                  LabReportsModel.specification, LabDetailModel.user_id,
                                                  LabDetailModel.address, LabDetailModel.latitude,
                                                  LabDetailModel.longitude, UserModel.name, UserModel.email,
                                                  UserModel.user_type, UserModel.phone_number, UserModel.gender,
                                                  UserModel.image, LabDetailModel.own_by, LabDetailModel.verified) \
                        .join(LabDetailModel, LabReportsModel.lab_detail_id == LabDetailModel.id)\
                        .join(UserModel, LabDetailModel.user_id == UserModel.id)\
                        .filter(UserModel.user_type == 'lab')
        if user_id:
            lab = lab.filter(LabDetailModel.user_id == user_id)
        if id:
            lab = lab.filter(LabReportsModel.id == id)
        if lab_detail_id:
            lab = lab.filter(LabReportsModel.lab_detail_id == lab_detail_id)

        lab = lab.all()
        return lab

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        LabReportsModel.query.filter(LabReportsModel.id == id).update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(id):
        LabReportsModel.query.filter(LabReportsModel.id == id).delete()
        db.session.commit()