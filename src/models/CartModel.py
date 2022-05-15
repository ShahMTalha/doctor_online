from . import db
import datetime
from .StoreMedicinesModel import StoreMedicinesModel
from .MedicineModel import MedicineModel
from .UserModel import UserModel
from sqlalchemy.orm import aliased


class CartModel(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    store_medicine_id = db.Column(db.Integer, db.ForeignKey(StoreMedicinesModel.id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, patient_id, store_id, store_medicine_id, quantity):
        self.patient_id = patient_id
        self.store_id = store_id
        self.store_medicine_id = store_medicine_id
        self.quantity = quantity
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_cart(user_id="", id="", store_medicine_id=""):
        Patient = aliased(UserModel)
        Store = aliased(UserModel)
        cart = CartModel.query.with_entities(CartModel.id, CartModel.patient_id, StoreMedicinesModel.medicine_id,
                                             CartModel.quantity, CartModel.store_id, StoreMedicinesModel.price,
                                             Patient.name.label("patient_name"), Store.name.label("store_name"),
                                             MedicineModel.name, MedicineModel.image) \
                        .join(StoreMedicinesModel, CartModel.store_medicine_id == StoreMedicinesModel.id)\
                        .join(MedicineModel, StoreMedicinesModel.medicine_id == MedicineModel.id)\
                        .join(Patient, CartModel.patient_id == Patient.id)\
                        .join(Store, CartModel.store_id == Store.id)
        if user_id:
            cart = cart.filter(CartModel.patient_id == user_id)
        if id:
            cart = cart.filter(CartModel.id == id)
        if store_medicine_id:
            cart = cart.filter(CartModel.store_medicine_id == store_medicine_id)

        cart = cart.all()
        return cart

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(cart_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        CartModel.query.filter(CartModel.id == cart_id).update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(id, patient_id):
        if id:
            CartModel.query.filter(CartModel.id == id).delete()
            db.session.commit()
        if patient_id:
            CartModel.query.filter(CartModel.patient_id == patient_id).delete()
            db.session.commit()