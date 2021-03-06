from . import db
import datetime
from .UserModel import UserModel
from sqlalchemy import func, text
from src.common.globals import geo_range


class StoreDetailModel(db.Model):
    __tablename__ = 'store_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    address = db.Column(db.String(), nullable=False)
    own_by = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    verified = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, address, own_by, latitude, longitude):
        self.user_id = user_id
        self.address = address
        self.own_by = own_by
        self.latitude = latitude
        self.longitude = longitude
        self.verified = 0
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_store(user_id="", name=None):
        store = UserModel.query.with_entities(StoreDetailModel.id, StoreDetailModel.user_id, UserModel.name,
                                            UserModel.email, StoreDetailModel.address, UserModel.user_type,
                                            UserModel.phone_number, UserModel.gender, UserModel.image,
                                            StoreDetailModel.own_by, StoreDetailModel.latitude,
                                            StoreDetailModel.longitude, StoreDetailModel.verified) \
                        .join(StoreDetailModel, UserModel.id == StoreDetailModel.user_id, isouter=True)\
                        .filter(UserModel.user_type == 'store')
        if user_id:
            store = store.filter(StoreDetailModel.user_id == user_id)
        if name:
            search = "%{}%".format(name.lower())
            store = store.filter(func.lower(UserModel.name).like(search))

        store = store.all()
        return store

    @staticmethod
    def get_store_by_location(lat, long, offset, limit, own_id):
        query = text("SELECT ld.id, ld.latitude, ld.longitude, ld.user_id, u.name, u.email, ld.address, u.image,\
                 distance FROM store_details ld inner join users u on ld.user_id = u.id CROSS JOIN LATERAL \
                (VALUES ( SQRT(POW(69.1 * (ld.latitude - " + str(lat) + "), 2) + POW(69.1 * (" + str(long) + " - ld.longitude) \
                * COS(ld.latitude / 57.3), 2)) )) v(distance) where v.distance < " + str(geo_range) + " and u.user_type = 'store' \
                and ld.user_id != " + str(own_id) + " \
                order by distance asc  limit " + str(limit) + " offset " + str(offset) + "")
        store = db.engine.execute(query).all()
        return store

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_user_id(user_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        StoreDetailModel.query.filter(StoreDetailModel.user_id == user_id).update(updated_data)
        db.session.commit()