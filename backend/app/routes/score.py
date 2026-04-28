from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import HealthScore
from datetime import date, timedelta

score_bp = Blueprint("score", __name__)


@score_bp.route("/latest", methods=["GET"])
@jwt_required()
def get_latest_score():
    user_id = int(get_jwt_identity())
    score = (
        HealthScore.query
        .filter_by(user_id=user_id)
        .order_by(HealthScore.computed_at.desc())
        .first()
    )
    if not score:
        return jsonify({"message": "No score computed yet", "score": None}), 200
    return jsonify({"score": score.to_dict()}), 200


@score_bp.route("/history", methods=["GET"])
@jwt_required()
def get_score_history():
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 30, type=int)
    since = date.today() - timedelta(days=days)

    scores = (
        HealthScore.query
        .filter(HealthScore.user_id == user_id, HealthScore.computed_at >= since)
        .order_by(HealthScore.computed_at.asc())
        .all()
    )
    return jsonify({"scores": [s.to_dict() for s in scores]}), 200
