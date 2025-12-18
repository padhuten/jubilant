# email_service.py

"""
Simple email sender using SMTP (Gmail default).
Supports both plain text and premium HTML emails.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, ADMIN_EMAIL
from typing import Optional
import re


def _strip_html(html: str) -> str:
    """Basic HTML → plain text fallback"""
    text = re.sub(r"<[^>]+>", "", html)
    return text.strip()


def send_email(
    subject: str,
    body: str,
    to_email: Optional[str] = None,
    is_html: bool = False,
    retry: int = 1
) -> bool:
    """
    Send an email using SMTP.
    - body: plain text OR HTML
    - is_html=True → sends premium HTML email
    """

    to_email = to_email or ADMIN_EMAIL

    if not SMTP_USER or not SMTP_PASS:
        print("⚠️ SMTP credentials not provided. Skipping email.", file=sys.stderr)
        return False

    # MULTIPART allows HTML + plain-text fallback
    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = to_email  # safe default; can be overridden later

    # Attach body
    if is_html:
        # Plain-text fallback first (email standard)
        msg.attach(MIMEText(_strip_html(body), "plain"))
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    attempt = 0
    while attempt <= retry:
        try:
            attempt += 1
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)

            print(f"📧 Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            print(f"❌ Email send attempt {attempt} failed: {e}", file=sys.stderr)
            if attempt > retry:
                return False

    return False
