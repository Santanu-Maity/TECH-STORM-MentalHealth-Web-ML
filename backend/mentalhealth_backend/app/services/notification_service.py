"""
notification_service.py
Sends appointment confirmation and reminder emails.
"""
from flask import current_app
from app import mail
from app.models import User
from flask_mail import Message


def send_appointment_confirmation(user_id: int, appointment, doctor) -> None:
    user = User.query.get(user_id)
    if not user:
        return

    name = (user.profile.full_name if user.profile and not appointment.is_anonymous else "User") or user.email

    try:
        msg = Message(
            subject="✅ Appointment Confirmed – MentalHealth App",
            recipients=[user.email],
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
            <h2 style="color: #388e3c;">✅ Appointment Confirmed</h2>
            <p>Hi <strong>{name}</strong>,</p>
            <p>Your appointment has been successfully booked. Here are the details:</p>
            <table style="border-collapse: collapse; width: 100%;">
                <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Doctor</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">Dr. {doctor.name}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Specialization</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{doctor.specialization}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Date</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{appointment.appointment_date}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Time</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{appointment.appointment_time}</td></tr>
                <tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Mode</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{appointment.mode.capitalize()}</td></tr>
            </table>
            <p style="margin-top:20px;">If you need to cancel, please do so at least 24 hours before the appointment.</p>
            <p>Take care of yourself. 💚</p>
            <hr/>
            <p style="color: #888; font-size: 12px;">TECH STORM MentalHealth App</p>
        </div>
        """
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send appointment confirmation: {e}")
