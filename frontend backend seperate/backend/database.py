# database.py
"""
PostgreSQL connection helpers.

Usage:
    from database import get_conn, get_cursor, conn, cur

Prefer calling get_cursor() in long-running processes to ensure a live cursor.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError, InterfaceError
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS
import time
import sys

# Module-level connection object (attempted at import time)
conn = None
cur = None

def _connect():
    """Make a fresh connection (raises on failure)."""
    if not all([DB_HOST, DB_NAME, DB_USER, DB_PASS]):
        raise RuntimeError("Database credentials not fully provided in environment.")
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )

def get_conn(retries: int = 3, backoff: float = 0.5):
    """
    Return a live connection object. Will attempt to reconnect a few times on failure.
    """
    global conn
    attempt = 0
    while True:
        try:
            if conn is None or conn.closed:
                conn = _connect()
            # quick sanity check
            with conn.cursor() as _c:
                _c.execute("SELECT 1;")
            return conn
        except Exception as e:
            attempt += 1
            print(f"🔁 DB connect attempt {attempt} failed: {e}", file=sys.stderr)
            conn = None
            if attempt >= retries:
                raise
            time.sleep(backoff * attempt)

def get_cursor(retries: int = 3, backoff: float = 0.5):
    """
    Return a (conn, cursor) tuple with a RealDictCursor.
    Caller should not close conn; but should close cursor when done.
    """
    connection = get_conn(retries=retries, backoff=backoff)
    try:
        cursor = connection.cursor()
        return connection, cursor
    except (OperationalError, InterfaceError) as e:
        # try one reconnect and recreate
        connection = get_conn(retries=retries, backoff=backoff)
        cursor = connection.cursor()
        return connection, cursor

# Create module-level conn/cur (best-effort; safe to import)
try:
    conn = get_conn(retries=1, backoff=0.1)
    cur = conn.cursor()
    print("🟢 database module: connected and cursor ready")
except Exception as e:
    print("⚠️  database module: initial connection failed:", e, file=sys.stderr)
    conn = None
    cur = None

def test_query():
    """Optional health check; returns True if DB responds."""
    try:
        c = cur or get_cursor()[1]
        c.execute("SELECT 1;")
        _ = c.fetchone()
        print("🟢 DB Test OK")
        return True
    except Exception as e:
        print("🔴 DB Test Failed:", e, file=sys.stderr)
        return False

if __name__ == "__main__":
    test_query()
