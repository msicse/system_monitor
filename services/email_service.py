from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from config import settings
import smtplib
import logging
from typing import Union, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def send_email(
    to_address: Union[str, List[str]],
    subject: str,
    body: str,
    html_body: Optional[str] = None,
    attachments: Optional[List[Union[str, Path]]] = None,
    cc: Optional[Union[str, List[str]]] = None,
    bcc: Optional[Union[str, List[str]]] = None,
    raise_on_error: bool = False
) -> bool:
    """Send an email with optional HTML, attachments, CC, and BCC.

    Args:
        to_address: Recipient email address(es). Can be a string or list of strings.
        subject: Email subject line.
        body: Plain text body content.
        html_body: Optional HTML version of the email body. If provided, email will be multipart.
        attachments: Optional list of file paths to attach. Can be strings or Path objects.
        cc: Optional CC recipient(s). Can be a string or list of strings.
        bcc: Optional BCC recipient(s). Can be a string or list of strings.
        raise_on_error: If True, re-raises exceptions after logging. If False, returns False on error.

    Returns:
        bool: True if email sent successfully, False if an error occurred (when raise_on_error=False).

    Raises:
        smtplib.SMTPException: If raise_on_error=True and SMTP error occurs.
        Exception: If raise_on_error=True and other error occurs.

    Example:
        >>> send_email(
        ...     to_address="user@example.com",
        ...     subject="Test",
        ...     body="Plain text content",
        ...     html_body="<h1>HTML content</h1>",
        ...     attachments=["report.pdf", "screenshot.png"],
        ...     cc="manager@example.com"
        ... )
        True
    """
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USER
    msg["Subject"] = subject

    # Handle multiple recipients
    def _format_addresses(addresses: Union[str, List[str], None]) -> Optional[str]:
        if addresses is None:
            return None
        if isinstance(addresses, str):
            return addresses
        return ", ".join(addresses)

    msg["To"] = _format_addresses(to_address)
    if cc:
        msg["Cc"] = _format_addresses(cc)
    if bcc:
        msg["Bcc"] = _format_addresses(bcc)

    # Set email content
    msg.set_content(body)
    
    # Add HTML alternative if provided
    if html_body:
        msg.add_alternative(html_body, subtype='html')

    # Add attachments if provided
    if attachments:
        for attachment_path in attachments:
            try:
                file_path = Path(attachment_path)
                if not file_path.exists():
                    logger.warning("Attachment not found: %s", file_path)
                    continue

                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    msg.add_attachment(
                        file_data,
                        maintype='application',
                        subtype='octet-stream',
                        filename=file_path.name
                    )
                logger.debug("Attached file: %s", file_path.name)
            except Exception as e:
                logger.warning("Failed to attach file %s: %s", attachment_path, e)

    try:
        # Connect with timeout for fast failure on network issues
        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=getattr(settings, 'SMTP_TIMEOUT', 10)
        ) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Email sent to %s (subject: %s)", to_address, subject)
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
