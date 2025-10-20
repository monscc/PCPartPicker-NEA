"""Tests for user account system"""
from pcbuilder.accounts import register, authenticate
from pcbuilder.db import DB_FILE, init_db
import sqlite3
from pathlib import Path


def clear_test_users():
    """Helper to clear test users"""
    init_db()  # Ensure tables exist
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username LIKE 'testuser%'")
    conn.commit()
    conn.close()


def test_register_new_user():
    clear_test_users()
    success, msg = register("testuser1", "password123")
    assert success is True
    assert "created" in msg.lower()


def test_register_duplicate_user():
    clear_test_users()
    register("testuser2", "password123")
    success, msg = register("testuser2", "password456")
    assert success is False
    assert "exists" in msg.lower()


def test_register_weak_password():
    success, msg = register("testuser3", "123")
    assert success is False
    assert "6 characters" in msg


def test_authenticate_success():
    clear_test_users()
    register("testuser4", "password123")
    success, user_id, msg = authenticate("testuser4", "password123")
    assert success is True
    assert user_id is not None
    assert "successful" in msg.lower()


def test_authenticate_wrong_password():
    clear_test_users()
    register("testuser5", "password123")
    success, user_id, msg = authenticate("testuser5", "wrongpass")
    assert success is False
    assert user_id is None
    assert "invalid" in msg.lower()


def test_authenticate_nonexistent_user():
    success, user_id, msg = authenticate("nonexistent", "password")
    assert success is False
    assert user_id is None
