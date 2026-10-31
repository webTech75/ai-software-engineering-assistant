"""
===============================================================================
File:
    app/services/email_service.py

Description:
    Email notification service.

Author:
    Amr Elhabbal
===============================================================================
"""

import sib_api_v3_sdk

from app.core.config import settings


def send_password_reset_email(
    recipient_email: str,
    reset_link: str,
):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.brevo_api_key

    api_client = sib_api_v3_sdk.ApiClient(configuration)

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

    email = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": "Neura AI SWEA",
            "email": settings.email_from,
        },
        to=[
            {
                "email": recipient_email,
            }
        ],
        subject="Reset your Neura AI password",
        html_content=f"""
             <div style="text-align:center;">
                <img 
                    src="https://neura-client.onrender.com/neura_icon.png"
                    alt="Neura Logo"
                    width="100"
                />
            </div>
            <p>Hello, this is Neura </p>

            <p>You requested a password reset for your Neura account.</p>

            <p>
            Click the link below to reset your password:
            </p>

            <p>
            <a href="{reset_link}">
                Reset Password
            </a>
            </p>

            <p>
            If you received this email by mistake or did not request a password reset,
            please ignore this message. No action is required.
            </p>

            <p>
            AI Software Engineering Assistant
            </p>
        """,
    )

    try:
        response = api_instance.send_transac_email(email)
        print("Password reset email sent successfully.")
        print(response)

    except Exception as e:
        print("Password reset email failed:")
        print(e)
        raise


def send_admin_notification_email(
    subject: str,
    content: str,
):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.brevo_api_key

    api_client = sib_api_v3_sdk.ApiClient(configuration)

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

    email = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": "Neura AI Software Engineering Assistant",
            "email": settings.email_from,
        },
        to=[
            {
                "email": settings.admin_email,
            }
        ],
        subject=subject,
        html_content=content,
    )

    api_instance.send_transac_email(email)
