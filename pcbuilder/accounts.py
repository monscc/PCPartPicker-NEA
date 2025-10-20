"""User account management module"""
from typing import Optional
from .db import create_user, login_user


def register(username: str, password: str) -> tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters"
    user_id = create_user(username, password)
    if user_id is None:
        return False, "Username already exists"
    return True, f"Account created with ID {user_id}"


def authenticate(username: str, password: str) -> tuple[bool, Optional[tuple], str]:
    """Authenticate a user. Returns (success, (user_id, role), message)."""
    result = login_user(username, password)
    if result is None:
        return False, None, "Invalid username or password"
    return True, result, "Login successful"
