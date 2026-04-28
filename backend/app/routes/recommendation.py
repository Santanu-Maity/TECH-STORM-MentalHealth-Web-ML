from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import HealthScore, MoodLog
from app.services.recommendation_service import get_personalized_recommendations

recommendation_bp = Blueprint("recommendation", __name__)


@recommendation_bp.route("/", methods=["GET"])
@jwt_required()
def get_recommendations():
    user_id = int(get_jwt_identity())

    latest_score = (
        HealthScore.query
        .filter_by(user_id=user_id)
        .order_by(HealthScore.computed_at.desc())
        .first()
    )
    latest_mood = (
        MoodLog.query
        .filter_by(user_id=user_id)
        .order_by(MoodLog.logged_at.desc())
        .first()
    )

    score_val = latest_score.score if latest_score else 50
    risk_level = latest_score.risk_level if latest_score else "moderate"

    recommendations = get_personalized_recommendations(score_val, risk_level, latest_mood)
    return jsonify(recommendations), 200


@recommendation_bp.route("/quotes", methods=["GET"])
@jwt_required()
def get_quotes():
    from app.services.recommendation_service import get_motivational_quotes
    mood = request.args.get("mood", "neutral")
    quotes = get_motivational_quotes(mood)
    return jsonify({"quotes": quotes}), 200


@recommendation_bp.route("/yoga", methods=["GET"])
@jwt_required()
def get_yoga():
    from app.services.recommendation_service import get_yoga_exercises
    level = request.args.get("level", "beginner")
    exercises = get_yoga_exercises(level)
    return jsonify({"exercises": exercises}), 200


@recommendation_bp.route("/music", methods=["GET"])
@jwt_required()
def get_music():
    from app.services.recommendation_service import get_music_recommendations
    mood = request.args.get("mood", "calm")
    music = get_music_recommendations(mood)
    return jsonify({"music": music}), 200


@recommendation_bp.route("/movies", methods=["GET"])
@jwt_required()
def get_movies():
    from app.services.recommendation_service import get_movie_recommendations
    mood = request.args.get("mood", "uplifting")
    movies = get_movie_recommendations(mood)
    return jsonify({"movies": movies}), 200


@recommendation_bp.route("/meditation", methods=["GET"])
@jwt_required()
def get_meditation():
    from app.services.recommendation_service import get_meditation_guides
    duration = request.args.get("duration", 10, type=int)
    guides = get_meditation_guides(duration)
    return jsonify({"guides": guides}), 200
