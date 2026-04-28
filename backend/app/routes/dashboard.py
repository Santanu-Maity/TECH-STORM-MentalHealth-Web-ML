from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import MoodLog, HealthScore
from sqlalchemy import func
from datetime import date, timedelta
from app import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_summary():
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 30, type=int)
    since = date.today() - timedelta(days=days)

    logs = MoodLog.query.filter(
        MoodLog.user_id == user_id,
        MoodLog.log_date >= since
    ).all()

    if not logs:
        return jsonify({"message": "No data yet", "summary": None}), 200

    avg_mood = sum(l.mood_rating for l in logs) / len(logs)
    avg_anxiety = sum(l.anxiety_level for l in logs) / len(logs)
    avg_sleep = sum(l.sleep_hours or 0 for l in logs) / len(logs)
    avg_energy = sum(l.energy_level or 5 for l in logs) / len(logs)
    total_activity = sum(l.physical_activity_minutes or 0 for l in logs)

    latest_score = (
        HealthScore.query
        .filter_by(user_id=user_id)
        .order_by(HealthScore.computed_at.desc())
        .first()
    )

    return jsonify({
        "summary": {
            "period_days": days,
            "total_logs": len(logs),
            "avg_mood": round(avg_mood, 2),
            "avg_anxiety": round(avg_anxiety, 2),
            "avg_sleep_hours": round(avg_sleep, 2),
            "avg_energy": round(avg_energy, 2),
            "total_activity_minutes": total_activity,
            "latest_health_score": latest_score.score if latest_score else None,
            "risk_level": latest_score.risk_level if latest_score else "unknown",
        }
    }), 200


@dashboard_bp.route("/mood-trend", methods=["GET"])
@jwt_required()
def mood_trend():
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 14, type=int)
    since = date.today() - timedelta(days=days)

    logs = (
        MoodLog.query
        .filter(MoodLog.user_id == user_id, MoodLog.log_date >= since)
        .order_by(MoodLog.log_date.asc())
        .all()
    )

    trend = [
        {
            "date": l.log_date.isoformat(),
            "mood_rating": l.mood_rating,
            "anxiety_level": l.anxiety_level,
            "energy_level": l.energy_level,
            "sleep_hours": l.sleep_hours,
        }
        for l in logs
    ]
    return jsonify({"trend": trend}), 200


@dashboard_bp.route("/score-trend", methods=["GET"])
@jwt_required()
def score_trend():
    user_id = int(get_jwt_identity())
    days = request.args.get("days", 30, type=int)
    since = date.today() - timedelta(days=days)

    scores = (
        HealthScore.query
        .filter(HealthScore.user_id == user_id, HealthScore.computed_at >= since)
        .order_by(HealthScore.computed_at.asc())
        .all()
    )
    return jsonify({
        "score_trend": [
            {
                "date": s.computed_at.date().isoformat(),
                "score": s.score,
                "risk_level": s.risk_level,
            }
            for s in scores
        ]
    }), 200


@dashboard_bp.route("/streak", methods=["GET"])
@jwt_required()
def get_streak():
    """Calculate how many consecutive days the user has logged mood."""
    user_id = int(get_jwt_identity())
    logs = (
        MoodLog.query
        .filter_by(user_id=user_id)
        .order_by(MoodLog.log_date.desc())
        .all()
    )

    streak = 0
    expected = date.today()
    for log in logs:
        if log.log_date == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif log.log_date < expected:
            break

    return jsonify({"streak_days": streak}), 200
