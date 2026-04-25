"""
tests/test_api.py
Run:  python -m pytest tests/ -v
"""
import json
import pytest
from app import create_app, db
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Register and login, return JWT auth headers."""
    client.post("/api/auth/register", json={"email": "test@test.com", "password": "testpass1"})
    resp = client.post("/api/auth/login", json={"email": "test@test.com", "password": "testpass1"})
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Auth Tests ────────────────────────────────────────────────────────────────

class TestAuth:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "new@test.com", "password": "password123"
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert "access_token" in data
        assert data["user"]["email"] == "new@test.com"

    def test_register_duplicate_email(self, client):
        client.post("/api/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
        resp = client.post("/api/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
        assert resp.status_code == 409

    def test_register_invalid_email(self, client):
        resp = client.post("/api/auth/register", json={"email": "not-an-email", "password": "pass1234"})
        assert resp.status_code == 400

    def test_register_short_password(self, client):
        resp = client.post("/api/auth/register", json={"email": "a@b.com", "password": "123"})
        assert resp.status_code == 400

    def test_login_success(self, client):
        client.post("/api/auth/register", json={"email": "login@test.com", "password": "mypassword"})
        resp = client.post("/api/auth/login", json={"email": "login@test.com", "password": "mypassword"})
        assert resp.status_code == 200
        assert "access_token" in resp.get_json()

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={"email": "u@test.com", "password": "rightpass"})
        resp = client.post("/api/auth/login", json={"email": "u@test.com", "password": "wrongpass"})
        assert resp.status_code == 401

    def test_get_me(self, client, auth_headers):
        resp = client.get("/api/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        assert "email" in resp.get_json()

    def test_protected_without_token(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401


# ── Profile Tests ─────────────────────────────────────────────────────────────

class TestProfile:
    def test_get_profile(self, client, auth_headers):
        resp = client.get("/api/profile/", headers=auth_headers)
        assert resp.status_code == 200

    def test_update_profile(self, client, auth_headers):
        resp = client.put("/api/profile/", headers=auth_headers, json={
            "full_name": "Santanu Maity",
            "age": 22,
            "gender": "male",
            "occupation": "Student",
            "location": "Kolkata",
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["profile"]["full_name"] == "Santanu Maity"
        assert data["profile"]["age"] == 22


# ── Mood Log Tests ────────────────────────────────────────────────────────────

class TestMoodLog:
    def _log_mood(self, client, headers, overrides=None):
        payload = {
            "mood_rating": 7,
            "anxiety_level": 3,
            "sleep_hours": 7.5,
            "sleep_quality": 8,
            "energy_level": 7,
            "social_interaction": 6,
            "stress_level": 4,
            "appetite": 8,
            "concentration": 7,
            "physical_activity_minutes": 30,
        }
        if overrides:
            payload.update(overrides)
        return client.post("/api/mood/", headers=headers, json=payload)

    def test_log_mood_success(self, client, auth_headers):
        resp = self._log_mood(client, auth_headers)
        assert resp.status_code == 201
        data = resp.get_json()
        assert "mood_log" in data
        assert "health_score" in data
        assert data["health_score"]["score"] >= 0

    def test_log_mood_missing_required(self, client, auth_headers):
        resp = client.post("/api/mood/", headers=auth_headers, json={"sleep_hours": 7})
        assert resp.status_code == 400

    def test_log_mood_invalid_range(self, client, auth_headers):
        resp = self._log_mood(client, auth_headers, {"mood_rating": 15})
        assert resp.status_code == 400

    def test_get_mood_logs(self, client, auth_headers):
        self._log_mood(client, auth_headers)
        resp = client.get("/api/mood/", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "mood_logs" in data
        assert len(data["mood_logs"]) >= 1

    def test_get_today_log(self, client, auth_headers):
        self._log_mood(client, auth_headers)
        resp = client.get("/api/mood/today", headers=auth_headers)
        assert resp.status_code == 200

    def test_delete_mood_log(self, client, auth_headers):
        resp = self._log_mood(client, auth_headers)
        log_id = resp.get_json()["mood_log"]["id"]
        del_resp = client.delete(f"/api/mood/{log_id}", headers=auth_headers)
        assert del_resp.status_code == 200


# ── Score Tests ───────────────────────────────────────────────────────────────

class TestScore:
    def test_no_score_yet(self, client, auth_headers):
        resp = client.get("/api/score/latest", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["score"] is None

    def test_score_after_mood_log(self, client, auth_headers):
        client.post("/api/mood/", headers=auth_headers, json={
            "mood_rating": 8, "anxiety_level": 2, "sleep_hours": 8,
            "sleep_quality": 9, "energy_level": 8, "stress_level": 2,
        })
        resp = client.get("/api/score/latest", headers=auth_headers)
        assert resp.status_code == 200
        score = resp.get_json()["score"]
        assert score is not None
        assert 0 <= score["score"] <= 100


# ── Recommendation Tests ──────────────────────────────────────────────────────

class TestRecommendations:
    def test_get_recommendations(self, client, auth_headers):
        resp = client.get("/api/recommendations/", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "coping_strategies" in data
        assert "yoga_exercises" in data
        assert "music" in data
        assert "movies" in data
        assert "quote" in data

    def test_get_quotes(self, client, auth_headers):
        resp = client.get("/api/recommendations/quotes?mood=neutral", headers=auth_headers)
        assert resp.status_code == 200
        assert "quotes" in resp.get_json()

    def test_get_meditation(self, client, auth_headers):
        resp = client.get("/api/recommendations/meditation?duration=10", headers=auth_headers)
        assert resp.status_code == 200
        assert "guides" in resp.get_json()


# ── Dashboard Tests ───────────────────────────────────────────────────────────

class TestDashboard:
    def test_summary_no_data(self, client, auth_headers):
        resp = client.get("/api/dashboard/summary", headers=auth_headers)
        assert resp.status_code == 200

    def test_streak_no_logs(self, client, auth_headers):
        resp = client.get("/api/dashboard/streak", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["streak_days"] == 0

    def test_streak_after_log(self, client, auth_headers):
        client.post("/api/mood/", headers=auth_headers, json={
            "mood_rating": 7, "anxiety_level": 3,
        })
        resp = client.get("/api/dashboard/streak", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()["streak_days"] == 1


# ── Emergency Tests ───────────────────────────────────────────────────────────

class TestEmergency:
    def test_crisis_resources_public(self, client):
        """Crisis resources endpoint is public (no auth)."""
        resp = client.get("/api/emergency/resources")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "resources" in data
        assert len(data["resources"]) > 0

    def test_alert_history_requires_auth(self, client):
        resp = client.get("/api/emergency/history")
        assert resp.status_code == 401
