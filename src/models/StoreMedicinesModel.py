from . import db
import datetime
from .StoreDetailModel import StoreDetailModel
from .MedicineModel import MedicineModel
from .UserModel import UserModel


class StoreMedicinesModel(db.Model):
    __tablename__ = 'store_medicines'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_detail_id = db.Column(db.Integer, db.ForeignKey(StoreDetailModel.id), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey(MedicineModel.id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, store_detail_id, medicine_id, quantity, price, description):
        self.store_detail_id = store_detail_id
        self.medicine_id = medicine_id
        self.quantity = quantity
        self.price = price
        self.description = description
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_store_medicines(user_id="", id="", store_detail_id=""):
        store = StoreMedicinesModel.query.with_entities(StoreMedicinesModel.id, StoreMedicinesModel.store_detail_id,
                                                        StoreMedicinesModel.medicine_id, StoreMedicinesModel.price,
                                                        StoreMedicinesModel.description, StoreDetailModel.user_id,
                                                        UserModel.name.label("store_name"),
                                                        MedicineModel.name.label("med_name"), MedicineModel.image,
                                                        MedicineModel.med_type, MedicineModel.weight,
                                                        StoreDetailModel.own_by, UserModel.user_type,
                                                        MedicineModel.company, MedicineModel.country) \
                        .join(StoreDetailModel, StoreMedicinesModel.store_detail_id == StoreDetailModel.id)\
                        .join(UserModel, StoreDetailModel.user_id == UserModel.id)\
                        .join(MedicineModel, StoreMedicinesModel.medicine_id == MedicineModel.id)\
                        .filter(UserModel.user_type == 'store')
        if user_id:
            store = store.filter(StoreDetailModel.user_id == user_id)
        if id:
            store = store.filter(StoreMedicinesModel.id == id)
        if store_detail_id:
            store = store.filter(StoreMedicinesModel.lab_detail_id == store_detail_id)

        store = store.all()
        return store

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        StoreMedicinesModel.query.filter(StoreMedicinesModel.id == id).update(updated_data)
        db.session.commit()

    @staticmethod
    def delete_by_id(id):
        StoreMedicinesModel.query.filter(StoreMedicinesModel.id == id).delete()
        db.session.commit()