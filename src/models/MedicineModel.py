from . import db
import datetime
from .UserModel import UserModel
from sqlalchemy import func


class MedicineModel(db.Model):
    __tablename__ = 'medicine'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
    name = db.Column(db.String(), nullable=False)
    company = db.Column(db.String(), nullable=False)
    med_type = db.Column(db.String(), nullable=False)
    weight = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, name, company, med_type, weight, country, image):
        self.user_id = user_id
        self.name = name
        self.company = company
        self.med_type = med_type
        self.weight = weight
        self.country = country
        self.image = image
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)


    @staticmethod
    def find_medicines(id="", user_id="", name="", med_type="", company=""):
        medicines = MedicineModel.query.with_entities(MedicineModel.id, MedicineModel.user_id, MedicineModel.name,
                                                      MedicineModel.company, MedicineModel.med_type,
                                                      MedicineModel.weight, MedicineModel.country, MedicineModel.image)
        if id:
            medicines = medicines.filter(MedicineModel.id == id)
        if name:
            search = "%{}%".format(name.lower())
            medicines = medicines.filter(func.lower(MedicineModel.name).like(search))
        if user_id:
            medicines = medicines.filter(MedicineModel.user_id == user_id)
        if company:
            search = "%{}%".format(company.lower())
            medicines = medicines.filter(func.lower(MedicineModel.company).like(search))
        if med_type:
            medicines = medicines.filter(func.lower(MedicineModel.med_type) == med_type.lower())

        medicines = medicines.all()
        return medicines
