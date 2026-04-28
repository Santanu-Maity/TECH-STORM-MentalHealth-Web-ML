from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import EmergencyAlert, User
from app.services.emergency_service import trigger_emergency_alert

emergency_bp = Blueprint("emergency", __name__)


@emergency_bp.route("/sos", methods=["POST"])
@jwt_required()
def manual_sos():
    """User manually triggers an SOS emergency alert."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    message = data.get("message", "User manually triggered SOS.")

    user = User.query.get_or_404(user_id)
    alert = trigger_emergency_alert(user, message=message, alert_type="manual_sos")
    return jsonify({
        "message": "Emergency alert sent to your contacts",
        "alert": alert.to_dict(),
    }), 200


@emergency_bp.route("/resources", methods=["GET"])
def get_crisis_resources():
    """Public endpoint - no login required."""
    resources = [
        {
            "name": "iCall (India)",
            "phone": "9152987821",
            "website": "https://icallhelpline.org",
            "description": "Psychosocial support helpline by TISS",
        },
        {
            "name": "Vandrevala Foundation Helpline",
            "phone": "1860-2662-345",
            "website": "https://www.vandrevalafoundation.com",
            "description": "24/7 free mental health support in India",
        },
        {
            "name": "NIMHANS (Bangalore)",
            "phone": "080-46110007",
            "website": "https://nimhans.ac.in",
            "description": "National Institute of Mental Health",
        },
        {
            "name": "Snehi (Delhi)",
            "phone": "011-65978181",
            "website": "https://snehi.org",
            "description": "Emotional support helpline",
        },
        {
            "name": "International Association for Suicide Prevention",
            "website": "https://www.iasp.info/resources/Crisis_Centres/",
            "description": "Global crisis centre directory",
        },
    ]
    return jsonify({"resources": resources}), 200


@emergency_bp.route("/history", methods=["GET"])
@jwt_required()
def get_alert_history():
    user_id = int(get_jwt_identity())
    alerts = (
        EmergencyAlert.query
        .filter_by(user_id=user_id)
        .order_by(EmergencyAlert.triggered_at.desc())
        .limit(20)
        .all()
    )
    return jsonify({"alerts": [a.to_dict() for a in alerts]}), 200
