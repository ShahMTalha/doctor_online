from . import db
import datetime
from .UserModel import UserModel


class RoasterModel(db.Model):
    __tablename__ = 'roaster'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    days = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, days, start_time, end_time):
        self.user_id = user_id
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_user_id(user_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        RoasterModel.query.filter(RoasterModel.user_id == user_id).update(updated_data)
        db.session.commit()

    @staticmethod
    def get_roaster(user_id):
        roaster = RoasterModel.query.with_entities(RoasterModel.id, RoasterModel.user_id, RoasterModel.days,
                                                    RoasterModel.start_time, RoasterModel.end_time)\
                                        .filter(RoasterModel.user_id == user_id).first()
        return roaster

    @staticmethod
    def delete_by_user_id(user_id):
        RoasterModel.query.filter(RoasterModel.user_id == user_id).delete()
        db.session.commit()