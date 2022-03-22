from . import db
from werkzeug.security import generate_password_hash

class Propertydb(db.Model):
    __tablename__ = 'Property'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_title = db.Column(db.String)
    description  = db.Column(db.String)
    no_of_rooms = db.Column(db.Integer)
    no_of_bathrooms = db.Column(db.Integer)
    price = db.Column(db.Float)
    property_type = db.Column(db.String)
    location = db.Column(db.String)
    photo = db.Column(db.String)

    def __init__(self, property_title, description, no_of_rooms, no_of_bathrooms, price, property_type, location, photo):
        self.property_title = property_title
        self.description = description
        self.no_of_rooms = no_of_rooms
        self.no_of_bathrooms = no_of_bathrooms
        self.price = price
        self.property_type = property_type
        self.location = location
        self.photo = photo