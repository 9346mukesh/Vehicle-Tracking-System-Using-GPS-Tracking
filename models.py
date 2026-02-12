"""
Database Models for Vehicle Tracking System
Supports SQLite with SQLAlchemy ORM
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')  # driver, customer, admin
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    rides_as_customer = db.relationship('Ride', foreign_keys='Ride.customer_id', backref='customer', lazy='dynamic')
    rides_as_driver = db.relationship('Ride', foreign_keys='Ride.driver_id', backref='driver', lazy='dynamic')
    vehicle = db.relationship('Vehicle', backref='owner', uselist=False, lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Vehicle(db.Model):
    """Vehicle model for driver vehicles"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    vehicle_type = db.Column(db.String(50))  # sedan, suv, auto, bike
    vehicle_model = db.Column(db.String(100))
    vehicle_color = db.Column(db.String(30))
    city = db.Column(db.String(50), default='bangalore')  # bangalore or porto
    current_lat = db.Column(db.Float)
    current_lon = db.Column(db.Float)
    status = db.Column(db.String(20), default='available')  # available, busy, offline
    rating = db.Column(db.Float, default=5.0)
    total_trips = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'vehicle_number': self.vehicle_number,
            'vehicle_type': self.vehicle_type,
            'vehicle_model': self.vehicle_model,
            'vehicle_color': self.vehicle_color,
            'city': self.city,
            'current_lat': self.current_lat,
            'current_lon': self.current_lon,
            'status': self.status,
            'rating': self.rating,
            'total_trips': self.total_trips
        }
    
    def __repr__(self):
        return f'<Vehicle {self.vehicle_number}>'


class Ride(db.Model):
    """Ride model for booking and tracking"""
    __tablename__ = 'rides'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Location details
    pickup_lat = db.Column(db.Float, nullable=False)
    pickup_lon = db.Column(db.Float, nullable=False)
    pickup_address = db.Column(db.String(255))
    dropoff_lat = db.Column(db.Float, nullable=False)
    dropoff_lon = db.Column(db.Float, nullable=False)
    dropoff_address = db.Column(db.String(255))
    
    # Trip details
    city = db.Column(db.String(50), default='bangalore')  # bangalore or porto
    distance = db.Column(db.Float)  # in kilometers
    duration = db.Column(db.Float)  # in minutes
    fare = db.Column(db.Float)  # in currency
    status = db.Column(db.String(20), default='pending')  # pending, accepted, in_progress, completed, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Rating and feedback
    rating = db.Column(db.Float)
    feedback = db.Column(db.Text)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'driver_id': self.driver_id,
            'pickup_lat': self.pickup_lat,
            'pickup_lon': self.pickup_lon,
            'pickup_address': self.pickup_address,
            'dropoff_lat': self.dropoff_lat,
            'dropoff_lon': self.dropoff_lon,
            'dropoff_address': self.dropoff_address,
            'city': self.city,
            'distance': self.distance,
            'duration': self.duration,
            'fare': self.fare,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'rating': self.rating,
            'feedback': self.feedback
        }
    
    def __repr__(self):
        return f'<Ride {self.id} - {self.status}>'


class SystemSettings(db.Model):
    """System-wide settings"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Setting {self.key}={self.value}>'
