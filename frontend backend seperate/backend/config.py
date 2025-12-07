# config.py
"""
Central configuration for the backend.

- Loads .env automatically.
- Exposes FRONTEND paths and SMTP defaults.
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# Base dirs
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = (BASE_DIR / ".." / "frontend").resolve()
TEMPLATES_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"

# Ensure frontend folders exist (warn, don't crash)
for p in (FRONTEND_DIR, TEMPLATES_DIR, STATIC_DIR):
    if not p.exists():
        print(f"⚠️  Warning: expected path not found: {p}", file=sys.stderr)

# SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "goguldev28@gmail.com")

# Database envs (read-only here)
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Simple validation helper (prints warnings; doesn't raise)
_missing = []
if not SMTP_USER or not SMTP_PASS:
    _missing.append("SMTP_USER/SMTP_PASS")
if not DB_HOST or not DB_NAME or not DB_USER or not DB_PASS:
    _missing.append("DB_HOST/DB_NAME/DB_USER/DB_PASS")
if _missing:
    print("⚠️  Missing required env vars (some features may fail):", ", ".join(_missing), file=sys.stderr)

__all__ = [
    "BASE_DIR", "FRONTEND_DIR", "TEMPLATES_DIR", "STATIC_DIR",
    "SMTP_SERVER", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "ADMIN_EMAIL",
    "DB_HOST", "DB_NAME", "DB_USER", "DB_PASS"
]
