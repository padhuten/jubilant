# email_service.py
"""
Simple email sender using SMTP (Gmail default).

Use:
    from email_service import send_email
"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, ADMIN_EMAIL
from typing import Optional

def send_email(subject: str, body: str, to_email: Optional[str] = None, retry: int = 1) -> bool:
    """
    Send an email using SMTP. Returns True on success, False otherwise.
    - If SMTP_USER or SMTP_PASS missing, function returns False (and prints a warning).
    - `to_email` defaults to ADMIN_EMAIL from config.
    """
    to_email = to_email or ADMIN_EMAIL

    if not SMTP_USER or not SMTP_PASS:
        print("⚠️  send_email: SMTP credentials not provided. Skipping send.", file=sys.stderr)
        return False

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
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
