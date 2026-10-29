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
            "name": "AI Software Engineering Assistant",
            "email": settings.email_from,
        },
        to=[
            {
                "email": recipient_email,
            }
        ],
        subject="Reset your password",
        html_content=f"""
                    <p>Hello,</p>

                    <p>You requested a password reset for your AI Software Engineering Assistant account.</p>

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
