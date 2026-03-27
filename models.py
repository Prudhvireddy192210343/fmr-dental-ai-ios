from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default="Doctor", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

class DoctorProfile(db.Model):
    __tablename__ = 'doctor_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fullName = db.Column(db.String(100), nullable=False)
    selectedSpecialty = db.Column(db.String(100), nullable=False)
    yearsOfExperience = db.Column(db.String(50), nullable=True)
    clinicName = db.Column(db.String(200), nullable=True)
    profileImageUrl = db.Column(db.Text, nullable=True)

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.String(50), primary_key=True)
    patientName = db.Column(db.String(100), nullable=False)
    patientId = db.Column(db.String(50), nullable=False)
    patientImageUrl = db.Column(db.Text, nullable=True)
    chiefComplaint = db.Column(db.Text, nullable=False)
    complaintType = db.Column(db.String(50), nullable=False)
    additionalDetails = db.Column(db.Text, nullable=True)
    medicalHistory = db.Column(db.Text, nullable=True)
    patientAge = db.Column(db.String(20), nullable=True)
    patientGender = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(50), default="active", nullable=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    doctorId = db.Column(db.String(50), nullable=False)
    doctorName = db.Column(db.String(100), nullable=False)
    
    # AI and Clinical Features as JSON
    clinicalFeatures = db.Column(db.JSON, nullable=True)
    lastAIResult = db.Column(db.JSON, nullable=True)

class AppNotification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    isNew = db.Column(db.Boolean, default=True)
