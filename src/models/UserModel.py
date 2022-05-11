from . import db
import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    user_type = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password, name, phone_number, gender, user_type, image):
        self.email = email
        self.password = password
        self.name = name
        self.phone_number = phone_number
        self.gender = gender
        self.user_type = user_type.lower()
        self.image = image
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_user(email="", user_id="", user_type=""):
        user = UserModel.query.with_entities(UserModel.id, UserModel.password, UserModel.email, UserModel.name,
                                             UserModel.user_type, UserModel.phone_number, UserModel.gender,
                                             UserModel.image)
        if email:
            user = user.filter(UserModel.email == email)
        if user_id:
            user = user.filter(UserModel.id == user_id)
        if user_type:
            user = user.filter(UserModel.user_type == user_type.lower())

        user = user.first()
        return user

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def update_by_id(user_id, updated_data):
        updated_data['modified_at'] = datetime.datetime.now()
        UserModel.query.filter(UserModel.id == user_id).update(updated_data)
        db.session.commit()