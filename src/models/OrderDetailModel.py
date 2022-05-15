from . import db
import datetime
from .StoreMedicinesModel import StoreMedicinesModel
from .MedicineModel import MedicineModel
from .OrderModel import OrderModel
from .UserModel import UserModel
from sqlalchemy.orm import aliased


class OrderDetailModel(db.Model):
    __tablename__ = 'order_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey(OrderModel.id), nullable=False)
    store_medicine_id = db.Column(db.Integer, db.ForeignKey(StoreMedicinesModel.id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, order_id, store_medicine_id, quantity):
        self.order_id = order_id
        self.store_medicine_id = store_medicine_id
        self.quantity = quantity
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_order(user_id="", id="", store_id=""):
        Patient = aliased(UserModel)
        Store = aliased(UserModel)
        order = OrderModel.query.with_entities(OrderDetailModel.id, OrderDetailModel.order_id, OrderDetailModel.quantity,
                                               OrderModel.patient_id, OrderModel.store_id, OrderModel.total,
                                               Patient.name.label("patient_name"), Store.name.label("store_name"),
                                               StoreMedicinesModel.medicine_id, StoreMedicinesModel.price,
                                               OrderModel.status,
                                               MedicineModel.name.label("med_name"), MedicineModel.image) \
            .join(OrderModel, OrderDetailModel.order_id == OrderModel.id)\
            .join(StoreMedicinesModel, OrderDetailModel.store_medicine_id == StoreMedicinesModel.id)\
            .join(MedicineModel, StoreMedicinesModel.medicine_id == MedicineModel.id)\
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
    def delete_by_id(order_id):
        OrderDetailModel.query.filter(OrderDetailModel.order_id == order_id).delete()
        db.session.commit()