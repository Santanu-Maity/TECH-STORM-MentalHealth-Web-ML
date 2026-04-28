from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import UserProfile

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    profile = UserProfile.query.filter_by(user_id=user_id).first_or_404()
    return jsonify(profile.to_dict()), 200


@profile_bp.route("/", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    profile = UserProfile.query.filter_by(user_id=user_id).first_or_404()
    data = request.get_json()

    allowed_fields = [
        "full_name", "age", "gender", "occupation", "location",
        "emergency_contact_name", "emergency_contact_phone",
        "emergency_contact_email", "pre_existing_conditions",
        "is_anonymous", "avatar_url",
    ]
    for field in allowed_fields:
        if field in data:
            setattr(profile, field, data[field])

    db.session.commit()
    return jsonify({"message": "Profile updated", "profile": profile.to_dict()}), 200
