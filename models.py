from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'client', 'worker', 'admin'
    
    # Relationships
    worker_profile = db.relationship('WorkerProfile', backref='user', uselist=False)
    client_bookings = db.relationship('Booking', foreign_keys='Booking.client_id', backref='client')
    worker_bookings = db.relationship('Booking', foreign_keys='Booking.worker_id', backref='worker')

class WorkerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_category = db.Column(db.String(50), nullable=False)
    experience_years = db.Column(db.Integer)
    location_lat = db.Column(db.Float)
    location_lon = db.Column(db.Float)
    is_approved = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=5.0)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, in_progress, completed, cancelled
    verification_code = db.Column(db.String(6))  # 6 digit OTP
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client': self.client.name,
            'worker': self.worker.name,
            'status': self.status,
            'date': self.created_at.strftime('%Y-%m-%d %H:%M')
        }
