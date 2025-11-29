from .database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

# parking lot
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

# parking spot
class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')
    spot_number = db.Column(db.String(20))

    lot = db.relationship('ParkingLot', backref=db.backref('spots', lazy=True, cascade="all, delete-orphan"))

# reservation
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=True)
    parking_cost_per_unit = db.Column(db.Float, nullable=False)
    vehicle_number = db.Column(db.String(50))
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), nullable=False, default='active')

    spot = db.relationship('ParkingSpot', backref=db.backref('reservations', lazy=True, cascade="all, delete-orphan"))
    user = db.relationship('User', backref=db.backref('reservations', lazy=True, cascade="all, delete-orphan"))



