from . import db
import datetime
from .StoreMedicinesModel import StoreMedicinesModel
from .UserModel import UserModel
from sqlalchemy.orm import aliased


class OrderModel(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, patient_id, store_id, total):
        self.patient_id = patient_id
        self.store_id = store_id
        self.total = total
        self.status = 'pending'
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_order(user_id="", id="", store_id=""):
        Patient = aliased(UserModel)
        Store = aliased(UserModel)
        order = OrderModel.query.with_entities(OrderModel.id, OrderModel.patient_id, OrderModel.total,
                                               OrderModel.store_id, OrderModel.status,
                                               Patient.name.label("patient_name"), Store.name.label("store_name")) \
            .join(Patient, OrderModel.patient_id == Patient.id)\
            .join(Store, OrderModel.store_id == Store.id)
        if user_id:
            order = order.filter(OrderModel.patient_id == user_id)
        if id:
            order = order.filter(OrderModel.id == id)
        if store_id:
            order = order.filter(OrderModel.store_id == store_id)

        order = order.all()
        return order

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(order_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        OrderModel.query.filter(OrderModel.id == order_id).update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(order_id):
        OrderModel.query.filter(OrderModel.id == order_id and OrderModel.status == 'pending').delete()
        db.session.commit()