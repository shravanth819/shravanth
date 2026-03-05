from .db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(50), default='farmer')
    location = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    phone_number = db.Column(db.String(20))
    
    # Preferences
    profile_picture = db.Column(db.String(255))
    default_crop_type = db.Column(db.String(100))
    preferred_language = db.Column(db.String(50), default='English')
    theme_preference = db.Column(db.String(20), default='dark')
    data_format = db.Column(db.String(20), default='metric')
    email_notifications = db.Column(db.Boolean, default=True)
    notifications_frequency = db.Column(db.String(50), default='immediate')
    critical_alerts_only = db.Column(db.Boolean, default=False)
    research_consent = db.Column(db.Boolean, default=False)
    data_sharing_consent = db.Column(db.Boolean, default=False)

class UserRegion(db.Model):
    __tablename__ = 'user_regions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    region_name = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    crop_type = db.Column(db.String(100))
    farm_area = db.Column(db.Float)
    is_favorite = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alert_type = db.Column(db.String(50))
    severity = db.Column(db.String(20))
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    data = db.Column(db.Text) # JSON string
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged_at = db.Column(db.DateTime)

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    region_name = db.Column(db.String(120))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    risk_score = db.Column(db.Float)
    data = db.Column(db.Text) # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemStatus(db.Model):
    __tablename__ = 'system_status'
    service_name = db.Column(db.String(100), primary_key=True)
    status = db.Column(db.String(50))
    response_time_ms = db.Column(db.Integer)
    last_check_time = db.Column(db.DateTime, default=datetime.utcnow)
    uptime_percentage = db.Column(db.Float)
    error_message = db.Column(db.Text)

class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))

class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_type = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    ip_address = db.Column(db.String(50))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    location = db.Column(db.String(200))
