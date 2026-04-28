from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from app import db
from app.models import User, UserProfile
from app.utils.validators import validate_email, validate_password

auth_bp = Blueprint("auth", __name__)

# In-memory blocklist for revoked tokens (use Redis in production)
BLOCKLIST = set()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not validate_email(email):
        return jsonify({"error": "Invalid email address"}), 400
    if not validate_password(password):
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Create empty profile
    profile = UserProfile(user_id=user.id)
    db.session.add(profile)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message": "Registration successful",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "profile_complete": bool(user.profile and user.profile.full_name),
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_token}), 200


@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = user.to_dict()
    if user.profile:
        data["profile"] = user.profile.to_dict()
    return jsonify(data), 200


@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    user = User.query.get_or_404(user_id)
    if not user.check_password(current_password):
        return jsonify({"error": "Current password is incorrect"}), 400
    if not validate_password(new_password):
        return jsonify({"error": "New password must be at least 8 characters"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200
