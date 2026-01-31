# Advanced Authentication and Authorization System
# Implements role-based access control (RBAC) with multiple user levels
from enum import Enum
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime
import functools


class UserRole(Enum):
    # Enumeration of user roles with two access levels
    GUEST = 0       # Read-only access, no save capability
    STANDARD = 1    # Full user with save/load builds
    
    def __lt__(self, other):
        # Enable role comparison for privilege checking
        if isinstance(other, UserRole):
            return self.value < other.value
        return NotImplemented
    
    def __le__(self, other):
        # Enable role comparison for privilege checking
        if isinstance(other, UserRole):
            return self.value <= other.value
        return NotImplemented


@dataclass
class Permission:
    # Defines a specific permission with metadata
    name: str
    description: str
    required_role: UserRole
    
    def check(self, user_role: UserRole) -> bool:
        # Check if a role has this permission
        return user_role.value >= self.required_role.value


class PermissionRegistry:
    # Singleton registry of all application permissions
    _instance = None
    _permissions: Dict[str, Permission] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, permission: Permission) -> None:
        # Register a new permission
        self._permissions[permission.name] = permission
    
    def get(self, name: str) -> Optional[Permission]:
        # Get a permission by name
        return self._permissions.get(name)
    
    def check(self, permission_name: str, user_role: UserRole) -> bool:
        # Check if a role has a specific permission
        perm = self.get(permission_name)
        if perm is None:
            return False
        return perm.check(user_role)
    
    def get_all_for_role(self, role: UserRole) -> List[Permission]:
        # Get all permissions available to a role
        return [p for p in self._permissions.values() if p.check(role)]


# Initialize permission registry and define permissions
_registry = PermissionRegistry()

# Define all application permissions
PERMISSIONS = {
    'VIEW_PARTS': Permission(
        'VIEW_PARTS',
        'View component catalog',
        UserRole.GUEST
    ),
    'BUILD_PC': Permission(
        'BUILD_PC',
        'Create and configure PC builds',
        UserRole.GUEST
    ),
    'CHECK_COMPATIBILITY': Permission(
        'CHECK_COMPATIBILITY',
        'Run compatibility checks',
        UserRole.GUEST
    ),
    'SAVE_BUILD': Permission(
        'SAVE_BUILD',
        'Save builds to database',
        UserRole.STANDARD
    ),
    'LOAD_BUILD': Permission(
        'LOAD_BUILD',
        'Load saved builds from database',
        UserRole.STANDARD
    ),
    'DELETE_BUILD': Permission(
        'DELETE_BUILD',
        'Delete saved builds',
        UserRole.STANDARD
    ),
}

# Register all permissions
for perm in PERMISSIONS.values():
    _registry.register(perm)


@dataclass
class User:
    # Represents an authenticated user with role and permissions
    user_id: Optional[int]
    username: str
    role: UserRole
    created_at: Optional[datetime] = None
    
    def has_permission(self, permission_name: str) -> bool:
        # Check if user has a specific permission
        return _registry.check(permission_name, self.role)
    
    def get_permissions(self) -> List[Permission]:
        # Get all permissions available to this user
        return _registry.get_all_for_role(self.role)
    
    def is_guest(self) -> bool:
        # Check if user is a guest
        return self.role == UserRole.GUEST
    
    def can_save(self) -> bool:
        # Convenience method to check save permission
        return self.has_permission('SAVE_BUILD')
    
    def can_load(self) -> bool:
        # Convenience method to check load permission
        return self.has_permission('LOAD_BUILD')


class GuestUser(User):
    # Singleton guest user instance
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not GuestUser._initialized:
            super().__init__(
                user_id=None,
                username="Guest",
                role=UserRole.GUEST,
                created_at=datetime.now()
            )
            GuestUser._initialized = True


def requires_permission(permission_name: str):
    # Decorator to enforce permission checking on methods
    #
    # Usage:
    # @requires_permission('SAVE_BUILD')
    # def save_build(self, build_data):
    # # Only executes if user has SAVE_BUILD permission
    # ...
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get current user from the object
            current_user = getattr(self, 'current_user', None)
            
            if current_user is None:
                raise PermissionError("No authenticated user")
            
            if not current_user.has_permission(permission_name):
                raise PermissionError(
                    f"User '{current_user.username}' (role: {current_user.role.name}) "
                    f"does not have permission: {permission_name}"
                )
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def requires_role(minimum_role: UserRole):
    # Decorator to enforce minimum role requirement
    #
    # Usage:
    # @requires_role(UserRole.STANDARD)
    # def standard_feature(self):
    # # Only executes if user is STANDARD level
    # ...
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            current_user = getattr(self, 'current_user', None)
            
            if current_user is None:
                raise PermissionError("No authenticated user")
            
            if current_user.role < minimum_role:
                raise PermissionError(
                    f"User '{current_user.username}' (role: {current_user.role.name}) "
                    f"requires minimum role: {minimum_role.name}"
                )
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class SessionManager:
    # Manages user sessions with singleton pattern
    _instance = None
    _current_user: Optional[User] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def login_guest(self) -> User:
        # Login as guest user
        self._current_user = GuestUser()
        return self._current_user
    
    def login_user(self, user_id: int, username: str, role: UserRole = UserRole.STANDARD) -> User:
        # Login as authenticated user
        self._current_user = User(
            user_id=user_id,
            username=username,
            role=role,
            created_at=datetime.now()
        )
        return self._current_user
    
    def logout(self) -> None:
        # Logout current user
        self._current_user = None
    
    def get_current_user(self) -> Optional[User]:
        # Get currently logged in user
        return self._current_user
    
    def is_logged_in(self) -> bool:
        # Check if any user is logged in
        return self._current_user is not None
    
    def require_login(self) -> User:
        # Get current user or raise exception
        if self._current_user is None:
            raise PermissionError("No user logged in")
        return self._current_user


# Global session manager instance
session = SessionManager()
