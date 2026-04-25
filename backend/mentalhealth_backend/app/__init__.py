from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.mood import mood_bp
    from app.routes.score import score_bp
    from app.routes.recommendation import recommendation_bp
    from app.routes.appointment import appointment_bp
    from app.routes.emergency import emergency_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(mood_bp, url_prefix="/api/mood")
    app.register_blueprint(score_bp, url_prefix="/api/score")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(emergency_bp, url_prefix="/api/emergency")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    with app.app_context():
        db.create_all()

    return app
