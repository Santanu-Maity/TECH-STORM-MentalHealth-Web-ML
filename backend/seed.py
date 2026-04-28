"""
seed.py — Seed the database with sample doctors and test user.
Run:  python seed.py
"""
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app
from app import db
from app.models import Doctor, User, UserProfile


DOCTORS = [
    {
        "name": "Priya Sharma",
        "specialization": "Psychiatry",
        "qualification": "MBBS, MD Psychiatry",
        "experience_years": 12,
        "email": "priya.sharma@hospital.com",
        "phone": "+91-9876543210",
        "hospital": "Apollo Hospitals",
        "location": "Kolkata",
        "consultation_fee": 800.0,
        "rating": 4.8,
        "available_slots": json.dumps({
            "Mon": ["10:00", "11:00", "14:00", "15:00"],
            "Wed": ["10:00", "11:00", "14:00"],
            "Fri": ["10:00", "11:00", "12:00"],
        }),
    },
    {
        "name": "Rajesh Kumar",
        "specialization": "Clinical Psychology",
        "qualification": "M.Phil Clinical Psychology, PhD",
        "experience_years": 8,
        "email": "rajesh.kumar@clinic.com",
        "phone": "+91-9123456789",
        "hospital": "NIMHANS Outreach Clinic",
        "location": "Kolkata",
        "consultation_fee": 600.0,
        "rating": 4.6,
        "available_slots": json.dumps({
            "Tue": ["09:00", "10:00", "11:00"],
            "Thu": ["09:00", "10:00", "15:00", "16:00"],
            "Sat": ["10:00", "11:00", "12:00"],
        }),
    },
    {
        "name": "Ananya Das",
        "specialization": "Counselling Psychologist",
        "qualification": "MA Psychology, Certified CBT Therapist",
        "experience_years": 5,
        "email": "ananya.das@therapy.com",
        "phone": "+91-9000012345",
        "hospital": "MindSpace Wellness Centre",
        "location": "Kolkata",
        "consultation_fee": 400.0,
        "rating": 4.9,
        "available_slots": json.dumps({
            "Mon": ["11:00", "12:00", "16:00", "17:00"],
            "Wed": ["11:00", "16:00", "17:00"],
            "Fri": ["11:00", "12:00", "16:00"],
            "Sat": ["10:00", "11:00"],
        }),
    },
    {
        "name": "Sanjay Mehta",
        "specialization": "Psychiatry",
        "qualification": "MBBS, DPM, DNB Psychiatry",
        "experience_years": 20,
        "email": "sanjay.mehta@medicalhub.com",
        "phone": "+91-9876001234",
        "hospital": "Medical Hub",
        "location": "Mumbai",
        "consultation_fee": 1200.0,
        "rating": 4.7,
        "available_slots": json.dumps({
            "Mon": ["09:00", "10:00"],
            "Tue": ["14:00", "15:00"],
            "Thu": ["09:00", "10:00", "11:00"],
        }),
    },
]


def seed():
    with app.app_context():
        db.create_all()

        # Seed doctors
        if Doctor.query.count() == 0:
            for d in DOCTORS:
                doctor = Doctor(**d)
                db.session.add(doctor)
            db.session.commit()
            print(f"✅ Seeded {len(DOCTORS)} doctors")
        else:
            print("⏭  Doctors already seeded")

        # Seed a test user
        if not User.query.filter_by(email="test@example.com").first():
            user = User(email="test@example.com")
            user.set_password("test1234")
            db.session.add(user)
            db.session.flush()

            profile = UserProfile(
                user_id=user.id,
                full_name="Test User",
                age=25,
                gender="prefer_not_to_say",
                occupation="Student",
                location="Kolkata",
                emergency_contact_email="emergency@example.com",
                emergency_contact_name="Emergency Contact",
            )
            db.session.add(profile)
            db.session.commit()
            print("✅ Test user created: test@example.com / test1234")
        else:
            print("⏭  Test user already exists")


if __name__ == "__main__":
    seed()
