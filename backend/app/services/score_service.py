"""
score_service.py
Computes a mental health score (0-100) from a MoodLog.
  - Attempts to load the trained ML model from disk.
  - Falls back to a weighted rule-based formula if the model is absent.
"""
import os
import pickle
import numpy as np
from flask import current_app
from app.models import HealthScore

_model = None
_scaler = None


def _load_model():
    global _model, _scaler
    if _model is not None:
        return

    model_path = current_app.config.get("ML_MODEL_PATH", "ml_model/mental_health_model.pkl")
    scaler_path = current_app.config.get("ML_SCALER_PATH", "ml_model/scaler.pkl")

    if os.path.exists(model_path) and os.path.exists(scaler_path):
        with open(model_path, "rb") as f:
            _model = pickle.load(f)
        with open(scaler_path, "rb") as f:
            _scaler = pickle.load(f)


def _mood_log_to_features(log) -> list:
    """Extract numeric features in the same order used during model training."""
    return [
        log.mood_rating or 5,
        log.anxiety_level or 5,
        log.sleep_hours or 7,
        log.sleep_quality or 5,
        log.energy_level or 5,
        log.social_interaction or 5,
        log.stress_level or 5,
        log.appetite or 5,
        log.concentration or 5,
        log.physical_activity_minutes or 0,
    ]


def _rule_based_score(features: list) -> float:
    """
    Weighted formula when ML model is not available.
    Higher score = better mental health (0-100).
    """
    (mood, anxiety, sleep_h, sleep_q, energy,
     social, stress, appetite, concentration, activity) = features

    # Positive contributions
    pos = (
        mood * 2.0 +
        sleep_q * 1.5 +
        energy * 1.5 +
        social * 1.0 +
        appetite * 1.0 +
        concentration * 1.0 +
        min(sleep_h, 9) * 1.5 +
        min(activity, 60) / 60 * 5
    )
    # Negative contributions
    neg = anxiety * 2.0 + stress * 1.5

    raw = (pos - neg)
    # Normalise to 0-100 based on theoretical min/max
    # pos_max ≈ 10*2+9*1.5+10*1.5+10+10+10+9*1.5+5 = 20+13.5+15+10+10+10+13.5+5 = 97
    # neg_max = 10*2+10*1.5 = 35  ⟹ raw in range [-35, 97]
    score = (raw + 35) / 132 * 100
    return float(max(0.0, min(100.0, score)))


def _classify_risk(score: float) -> str:
    if score >= 70:
        return "low"
    elif score >= 50:
        return "moderate"
    elif score >= 30:
        return "high"
    else:
        return "critical"


def compute_health_score(user_id: int, mood_log) -> HealthScore:
    """
    Main entry point called after a mood log is saved.
    Returns an unsaved HealthScore ORM object.
    """
    _load_model()
    features = _mood_log_to_features(mood_log)

    if _model is not None and _scaler is not None:
        X = np.array(features).reshape(1, -1)
        X_scaled = _scaler.transform(X)
        prediction = _model.predict(X_scaled)[0]
        confidence = float(max(_model.predict_proba(X_scaled)[0]))
        # Map prediction label to score (adjust labels to match your trained model)
        label_to_score = {
            "excellent": 90, "good": 75, "moderate": 55,
            "poor": 35, "critical": 15,
        }
        score = float(label_to_score.get(str(prediction).lower(), 50))
        ml_prediction = str(prediction)
        ml_confidence = confidence
    else:
        score = _rule_based_score(features)
        ml_prediction = "rule_based"
        ml_confidence = 1.0

    return HealthScore(
        user_id=user_id,
        mood_log_id=mood_log.id,
        score=round(score, 2),
        risk_level=_classify_risk(score),
        ml_prediction=ml_prediction,
        ml_confidence=round(ml_confidence, 4),
    )
