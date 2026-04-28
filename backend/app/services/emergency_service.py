"""
emergency_service.py
Handles automatic and manual emergency alert triggering.
"""
import json
from flask import current_app
from app import db, mail
from app.models import EmergencyAlert, User, UserProfile
from flask_mail import Message


def trigger_emergency_alert(user: User, message: str, alert_type: str = "auto_triggered") -> EmergencyAlert:
    profile: UserProfile = user.profile
    contacts = []

    if profile and profile.emergency_contact_email:
        contacts.append(profile.emergency_contact_email)
        _send_emergency_email(
            to=profile.emergency_contact_email,
            contact_name=profile.emergency_contact_name or "Emergency Contact",
            user_name=profile.full_name or user.email,
            message=message,
        )

    # Also notify admin/platform emergency team
    admin_email = current_app.config.get("EMERGENCY_CONTACT_EMAIL")
    if admin_email:
        contacts.append(admin_email)
        _send_emergency_email(
            to=admin_email,
            contact_name="Support Team",
            user_name=profile.full_name or user.email if profile else user.email,
            message=message,
        )

    alert = EmergencyAlert(
        user_id=user.id,
        alert_type=alert_type,
        message=message,
        notified_contacts=json.dumps(contacts),
    )
    db.session.add(alert)
    db.session.commit()
    return alert


def check_and_trigger_emergency(user_id: int, health_score) -> None:
    """Auto-trigger emergency if score falls below critical threshold."""
    threshold = current_app.config.get("RISK_SCORE_THRESHOLD", 30)
    if health_score.score <= threshold:
        user = User.query.get(user_id)
        if user:
            trigger_emergency_alert(
                user,
                message=f"Automated alert: Mental health score dropped to {health_score.score:.1f} (critical level).",
                alert_type="auto_triggered",
            )


def _send_emergency_email(to: str, contact_name: str, user_name: str, message: str):
    try:
        msg = Message(
            subject="⚠️ Mental Health Emergency Alert",
            recipients=[to],
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
            <h2 style="color: #d32f2f;">🚨 Emergency Alert</h2>
            <p>Dear <strong>{contact_name}</strong>,</p>
            <p>This is an automated message from the MentalHealth App regarding <strong>{user_name}</strong>.</p>
            <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0;">
                <p><strong>Alert:</strong> {message}</p>
            </div>
            <p>Please reach out to {user_name} as soon as possible to check on their wellbeing.</p>
            <p>If you believe they are in immediate danger, please contact local emergency services (112 in India).</p>
            <hr/>
            <p style="color: #888; font-size: 12px;">This is an automated alert from TECH STORM MentalHealth App.</p>
        </div>
        """
        mail.send(msg)
    except Exception as e:
        # Log but don't crash — email failure shouldn't break the flow
        current_app.logger.error(f"Failed to send emergency email to {to}: {e}")
