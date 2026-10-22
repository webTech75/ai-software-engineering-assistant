import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_password_reset_email(
    recipient_email: str,
    reset_link: str,
):
    message = EmailMessage()

    message["Subject"] = "Reset your password"
    message["From"] = settings.email_from
    message["To"] = recipient_email

    message.set_content(
        f"""
        Hello,

        You requested a password reset for your AI Software Engineering Assistant account.

        Click the link below to reset your password:

        {reset_link}

        If you did not request this password reset, you can ignore this email.

        AI Software Engineering Assistant
        """
    )
    
    print("SMTP HOST:", settings.email_host)
    print("SMTP PORT:", settings.email_port)
    print("SMTP USER:", settings.email_username)
    print("SMTP FROM:", settings.email_from)
    print("ABOUT TO CONNECT SMTP")
    with smtplib.SMTP(
        settings.email_host,
        settings.email_port,
        timeout=10,
    ) as server:

        server.starttls()

        server.login(
            settings.email_username,
            settings.email_password,
        )
        
        print("SMTP LOGIN SUCCESS")

        server.send_message(message)
        print("EMAIL SENT")