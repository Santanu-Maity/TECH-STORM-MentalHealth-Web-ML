from datetime import datetime, date
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = db.relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    mood_logs = db.relationship("MoodLog", back_populates="user", cascade="all, delete-orphan")
    health_scores = db.relationship("HealthScore", back_populates="user", cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat(),
        }


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))  # male, female, non_binary, prefer_not_to_say
    occupation = db.Column(db.String(100))
    location = db.Column(db.String(100))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_email = db.Column(db.String(120))
    pre_existing_conditions = db.Column(db.Text)   # comma-separated or JSON string
    is_anonymous = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="profile")

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "occupation": self.occupation,
            "location": self.location,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "emergency_contact_email": self.emergency_contact_email,
            "pre_existing_conditions": self.pre_existing_conditions,
            "is_anonymous": self.is_anonymous,
            "avatar_url": self.avatar_url,
        }


class MoodLog(db.Model):
    __tablename__ = "mood_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Core PHQ-9 / mood factors (1-10 scale unless specified)
    mood_rating = db.Column(db.Integer, nullable=False)          # 1 (very low) - 10 (excellent)
    anxiety_level = db.Column(db.Integer, nullable=False)        # 1 (none) - 10 (severe)
    sleep_hours = db.Column(db.Float)                            # hours of sleep
    sleep_quality = db.Column(db.Integer)                        # 1-10
    energy_level = db.Column(db.Integer)                         # 1-10
    social_interaction = db.Column(db.Integer)                   # 1-10
    stress_level = db.Column(db.Integer)                         # 1-10
    appetite = db.Column(db.Integer)                             # 1-10
    concentration = db.Column(db.Integer)                        # 1-10
    physical_activity_minutes = db.Column(db.Integer, default=0)
    # Free-text
    journal_entry = db.Column(db.Text)
    triggers = db.Column(db.Text)                                # what triggered mood
    gratitude_note = db.Column(db.Text)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    log_date = db.Column(db.Date, default=date.today)

    user = db.relationship("User", back_populates="mood_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "mood_rating": self.mood_rating,
            "anxiety_level": self.anxiety_level,
            "sleep_hours": self.sleep_hours,
            "sleep_quality": self.sleep_quality,
            "energy_level": self.energy_level,
            "social_interaction": self.social_interaction,
            "stress_level": self.stress_level,
            "appetite": self.appetite,
            "concentration": self.concentration,
            "physical_activity_minutes": self.physical_activity_minutes,
            "journal_entry": self.journal_entry,
            "triggers": self.triggers,
            "gratitude_note": self.gratitude_note,
            "log_date": self.log_date.isoformat() if self.log_date else None,
            "logged_at": self.logged_at.isoformat(),
        }


class HealthScore(db.Model):
    __tablename__ = "health_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mood_log_id = db.Column(db.Integer, db.ForeignKey("mood_logs.id"), nullable=True)
    score = db.Column(db.Float, nullable=False)          # 0-100
    risk_level = db.Column(db.String(20))                # low, moderate, high, critical
    ml_prediction = db.Column(db.String(50))             # model output label
    ml_confidence = db.Column(db.Float)                  # 0.0 - 1.0
    computed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="health_scores")

    def to_dict(self):
        return {
            "id": self.id,
            "score": self.score,
            "risk_level": self.risk_level,
            "ml_prediction": self.ml_prediction,
            "ml_confidence": self.ml_confidence,
            "computed_at": self.computed_at.isoformat(),
        }


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    qualification = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    hospital = db.Column(db.String(150))
    location = db.Column(db.String(100))
    available_slots = db.Column(db.Text)    # JSON string: {"Mon": ["10:00","11:00"]}
    consultation_fee = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    profile_image_url = db.Column(db.String(255))

    appointments = db.relationship("Appointment", back_populates="doctor")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "qualification": self.qualification,
            "experience_years": self.experience_years,
            "hospital": self.hospital,
            "location": self.location,
            "consultation_fee": self.consultation_fee,
            "rating": self.rating,
            "profile_image_url": self.profile_image_url,
        }


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)   # "HH:MM"
    mode = db.Column(db.String(20), default="online")              # online, in_person
    is_anonymous = db.Column(db.Boolean, default=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")           # pending, confirmed, cancelled, completed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")

    def to_dict(self):
        return {
            "id": self.id,
            "doctor": self.doctor.to_dict() if self.doctor else None,
            "appointment_date": self.appointment_date.isoformat(),
            "appointment_time": self.appointment_time,
            "mode": self.mode,
            "is_anonymous": self.is_anonymous,
            "reason": self.reason,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class EmergencyAlert(db.Model):
    __tablename__ = "emergency_alerts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    health_score = db.Column(db.Float)
    alert_type = db.Column(db.String(50))    # auto_triggered, manual_sos
    message = db.Column(db.Text)
    notified_contacts = db.Column(db.Text)   # JSON array of emails/phones
    resolved = db.Column(db.Boolean, default=False)
    triggered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "alert_type": self.alert_type,
            "message": self.message,
            "resolved": self.resolved,
            "triggered_at": self.triggered_at.isoformat(),
        }
