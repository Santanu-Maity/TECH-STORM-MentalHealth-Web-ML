from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import MoodLog, HealthScore
from app.services.score_service import compute_health_score
from app.services.emergency_service import check_and_trigger_emergency

mood_bp = Blueprint("mood", __name__)


@mood_bp.route("/", methods=["POST"])
@jwt_required()
def log_mood():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    required = ["mood_rating", "anxiety_level"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Validate ranges 1-10
    for field in ["mood_rating", "anxiety_level", "sleep_quality", "energy_level",
                  "social_interaction", "stress_level", "appetite", "concentration"]:
        val = data.get(field)
        if val is not None and not (1 <= int(val) <= 10):
            return jsonify({"error": f"'{field}' must be between 1 and 10"}), 400

    log = MoodLog(
        user_id=user_id,
        mood_rating=data["mood_rating"],
        anxiety_level=data["anxiety_level"],
        sleep_hours=data.get("sleep_hours"),
        sleep_quality=data.get("sleep_quality"),
        energy_level=data.get("energy_level"),
        social_interaction=data.get("social_interaction"),
        stress_level=data.get("stress_level"),
        appetite=data.get("appetite"),
        concentration=data.get("concentration"),
        physical_activity_minutes=data.get("physical_activity_minutes", 0),
        journal_entry=data.get("journal_entry"),
        triggers=data.get("triggers"),
        gratitude_note=data.get("gratitude_note"),
        log_date=date.today(),
    )
    db.session.add(log)
    db.session.flush()

    # Compute health score from this mood log
    score_obj = compute_health_score(user_id, log)
    db.session.add(score_obj)
    db.session.commit()

    # Check if emergency alert needed
    check_and_trigger_emergency(user_id, score_obj)

    return jsonify({
        "message": "Mood logged successfully",
        "mood_log": log.to_dict(),
        "health_score": score_obj.to_dict(),
    }), 201


@mood_bp.route("/", methods=["GET"])
@jwt_required()
def get_mood_logs():
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 30, type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    since = date.today() - timedelta(days=days)
    pagination = (
        MoodLog.query
        .filter(MoodLog.user_id == user_id, MoodLog.log_date >= since)
        .order_by(MoodLog.logged_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "mood_logs": [m.to_dict() for m in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
    }), 200


@mood_bp.route("/<int:log_id>", methods=["GET"])
@jwt_required()
def get_single_log(log_id):
    user_id = int(get_jwt_identity())
    log = MoodLog.query.filter_by(id=log_id, user_id=user_id).first_or_404()
    return jsonify(log.to_dict()), 200


@mood_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
def delete_log(log_id):
    user_id = int(get_jwt_identity())
    log = MoodLog.query.filter_by(id=log_id, user_id=user_id).first_or_404()
    db.session.delete(log)
    db.session.commit()
    return jsonify({"message": "Log deleted"}), 200


@mood_bp.route("/today", methods=["GET"])
@jwt_required()
def get_today_log():
    user_id = int(get_jwt_identity())
    log = MoodLog.query.filter_by(user_id=user_id, log_date=date.today()).first()
    if not log:
        return jsonify({"message": "No mood log for today", "mood_log": None}), 200
    return jsonify({"mood_log": log.to_dict()}), 200
