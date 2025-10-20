"""
User account management module with OOP design
Provides backward-compatible interface to AuthenticationService
"""
from typing import Optional
from .auth_service import get_auth_service


# Get singleton auth service instance
_auth_service = get_auth_service()


def register(username: str, password: str) -> tuple[bool, str]:
    """
    Register a new user
    Returns: (success, message)
    """
    return _auth_service.register_user(username, password)


def authenticate(username: str, password: str) -> tuple[bool, Optional[tuple], str]:
    """
    Authenticate a user
    Returns: (success, (user_id, role), message)
    """
    success, message = _auth_service.login(username, password)
    
    if success:
        user_id = _auth_service.get_current_user_id()
        role = _auth_service.get_current_role()
        return True, (user_id, role.value), message
    
    return False, None, message
