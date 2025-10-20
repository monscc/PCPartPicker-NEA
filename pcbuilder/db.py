import sqlite3
from pathlib import Path
import json
import hashlib
import secrets
import string
from typing import List, Optional, Dict
from datetime import datetime


DB_FILE = Path(__file__).resolve().parent.parent / "pcbuilder.db"


def init_db(db_path: Path = DB_FILE):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS parts (
        id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        attributes TEXT
    )
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role INTEGER DEFAULT 1,
        created_at TEXT
    )
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS builds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        parts_json TEXT,
        created_at TEXT,
        share_key TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )
    conn.commit()
    conn.close()


def load_sample_parts(json_path: Path) -> None:
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data:
        cur.execute(
            "INSERT OR REPLACE INTO parts (id, name, category, price, attributes) VALUES (?, ?, ?, ?, ?)",
            (p["id"], p["name"], p["category"], p["price"], json.dumps(p.get("attributes", {}))),
        )
    conn.commit()
    conn.close()


def list_parts() -> List[dict]:
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price, attributes FROM parts")
    rows = cur.fetchall()
    conn.close()
    parts = []
    for r in rows:
        parts.append({"id": r[0], "name": r[1], "category": r[2], "price": r[3], "attributes": json.loads(r[4]) if r[4] else {}})
    return parts


# --- User account functions ---


def hash_password(password: str) -> str:
    """Hash password using SHA256 (for demo; production should use bcrypt)"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, password: str, role: int = 1) -> Optional[int]:
    """Create a new user account. Returns user_id on success, None if username exists.
    
    Args:
        username: Unique username
        password: Plain text password (will be hashed)
        role: User role level (0=Guest, 1=Standard, 2=Premium, 3=Admin)
    """
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    pw_hash = hash_password(password)
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
            (username, pw_hash, role, datetime.now().isoformat()),
        )
        conn.commit()
        user_id = cur.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def login_user(username: str, password: str) -> Optional[tuple]:
    """Verify credentials. Returns (user_id, role) on success, None on failure."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    user_id, stored_hash, role = row
    if hash_password(password) == stored_hash:
        return (user_id, role)
    return None


# --- Build persistence functions ---

def generate_share_key() -> str:
    """Generate a unique 8-character share key"""
    # Use uppercase letters and digits for easy sharing
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))


def save_build(user_id: int, build_name: str, parts: Dict[str, Optional[Dict]]) -> tuple:
    """Save a build for a user. Returns (build_id, share_key)."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Generate unique share key
    share_key = generate_share_key()
    
    # Ensure uniqueness (very unlikely collision, but check anyway)
    while True:
        cur.execute("SELECT id FROM builds WHERE share_key = ?", (share_key,))
        if cur.fetchone() is None:
            break
        share_key = generate_share_key()
    
    cur.execute(
        "INSERT INTO builds (user_id, name, parts_json, created_at, share_key) VALUES (?, ?, ?, ?, ?)",
        (user_id, build_name, json.dumps(parts), datetime.now().isoformat(), share_key),
    )
    conn.commit()
    build_id = cur.lastrowid
    conn.commit()
    build_id = cur.lastrowid
    conn.close()
    return (build_id, share_key)


def load_user_builds(user_id: int) -> List[Dict]:
    """Load all builds for a user."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, parts_json, created_at, share_key FROM builds WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    builds = []
    for r in rows:
        builds.append({"id": r[0], "name": r[1], "parts": json.loads(r[2]), "created_at": r[3], "share_key": r[4]})
    return builds


def load_build_by_id(build_id: int) -> Optional[Dict]:
    """Load a specific build by ID."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, name, parts_json, created_at, share_key FROM builds WHERE id = ?", (build_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return {"id": row[0], "user_id": row[1], "name": row[2], "parts": json.loads(row[3]), "created_at": row[4], "share_key": row[5]}


def load_build_by_share_key(share_key: str) -> Optional[Dict]:
    """Load a build by its share key."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, name, parts_json, created_at, share_key FROM builds WHERE share_key = ?", (share_key,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return {"id": row[0], "user_id": row[1], "name": row[2], "parts": json.loads(row[3]), "created_at": row[4], "share_key": row[5]}


def import_build_from_share_key(user_id: int, share_key: str) -> Optional[tuple]:
    """Import a build from a share key to the user's account. Returns (build_id, share_key) on success."""
    build = load_build_by_share_key(share_key)
    if build is None:
        return None
    
    # Create a copy for the new user
    build_name = f"{build['name']} (imported)"
    parts = build['parts']
    
    # Save as new build for this user
    return save_build(user_id, build_name, parts)

