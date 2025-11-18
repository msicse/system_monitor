from email.message import EmailMessage
from config import settings
import smtplib
import logging

logger = logging.getLogger(__name__)


def send_email(to_address, subject, body, raise_on_error: bool = False) -> bool:
    
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        # give a short timeout so the call fails fast on network issues
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=getattr(settings, 'SMTP_TIMEOUT', 10)) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Email sent to %s", to_address)
        return True

    except smtplib.SMTPException as e:
        logger.exception("SMTP error sending email to %s: %s", to_address, e)
        if raise_on_error:
            raise
        return False

    except Exception as e:
        logger.exception("Unexpected error sending email to %s: %s", to_address, e)
        if raise_on_error:
            raise
        return False
