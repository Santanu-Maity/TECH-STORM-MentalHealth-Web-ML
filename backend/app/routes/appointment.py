from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Appointment, Doctor
from datetime import date

appointment_bp = Blueprint("appointment", __name__)


@appointment_bp.route("/doctors", methods=["GET"])
@jwt_required()
def list_doctors():
    specialization = request.args.get("specialization")
    location = request.args.get("location")

    query = Doctor.query.filter_by(is_active=True)
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    if location:
        query = query.filter(Doctor.location.ilike(f"%{location}%"))

    doctors = query.order_by(Doctor.rating.desc()).all()
    return jsonify({"doctors": [d.to_dict() for d in doctors]}), 200


@appointment_bp.route("/doctors/<int:doctor_id>", methods=["GET"])
@jwt_required()
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = doctor.to_dict()
    data["available_slots"] = doctor.available_slots   # raw JSON string
    data["email"] = doctor.email
    data["phone"] = doctor.phone
    return jsonify(data), 200


@appointment_bp.route("/", methods=["POST"])
@jwt_required()
def book_appointment():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    required = ["doctor_id", "appointment_date", "appointment_time"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    doctor = Doctor.query.get(data["doctor_id"])
    if not doctor or not doctor.is_active:
        return jsonify({"error": "Doctor not available"}), 404

    try:
        appt_date = date.fromisoformat(data["appointment_date"])
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if appt_date < date.today():
        return jsonify({"error": "Cannot book appointment in the past"}), 400

    # Check for duplicate slot
    existing = Appointment.query.filter_by(
        doctor_id=data["doctor_id"],
        appointment_date=appt_date,
        appointment_time=data["appointment_time"],
        status="confirmed",
    ).first()
    if existing:
        return jsonify({"error": "This slot is already booked"}), 409

    appt = Appointment(
        user_id=user_id,
        doctor_id=data["doctor_id"],
        appointment_date=appt_date,
        appointment_time=data["appointment_time"],
        mode=data.get("mode", "online"),
        is_anonymous=data.get("is_anonymous", False),
        reason=data.get("reason"),
        status="pending",
    )
    db.session.add(appt)
    db.session.commit()

    # Send confirmation email
    from app.services.notification_service import send_appointment_confirmation
    send_appointment_confirmation(user_id, appt, doctor)

    return jsonify({
        "message": "Appointment booked successfully",
        "appointment": appt.to_dict(),
    }), 201


@appointment_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_appointments():
    user_id = int(get_jwt_identity())
    status = request.args.get("status")
    query = Appointment.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    return jsonify({"appointments": [a.to_dict() for a in appointments]}), 200


@appointment_bp.route("/<int:appt_id>", methods=["DELETE"])
@jwt_required()
def cancel_appointment(appt_id):
    user_id = int(get_jwt_identity())
    appt = Appointment.query.filter_by(id=appt_id, user_id=user_id).first_or_404()

    if appt.status in ("completed", "cancelled"):
        return jsonify({"error": f"Cannot cancel a {appt.status} appointment"}), 400

    appt.status = "cancelled"
    db.session.commit()
    return jsonify({"message": "Appointment cancelled"}), 200
