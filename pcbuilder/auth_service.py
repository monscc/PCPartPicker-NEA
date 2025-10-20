"""
Authentication Service with Object-Oriented Design
Implements: Strategy pattern, Encapsulation, Abstraction
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from enum import Enum
from .custom_hash import my_custom_sha256_hash
from .database_manager import get_database_manager


class UserRole(Enum):
    """User role enumeration with hierarchical levels"""
    GUEST = 0
    STANDARD = 1
    PREMIUM = 2
    ADMIN = 3
    
    def __lt__(self, other):
        if isinstance(other, UserRole):
            return self.value < other.value
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, UserRole):
            return self.value <= other.value
        return NotImplemented


class PasswordHashStrategy(ABC):
    """
    Abstract base class for password hashing strategies
    Demonstrates: Strategy pattern, Abstraction
    """
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against a hash"""
        pass


class CustomSHA256Strategy(PasswordHashStrategy):
    """Custom SHA256 hashing strategy"""
    
    def hash_password(self, password: str) -> str:
        """Hash password using custom SHA256"""
        return my_custom_sha256_hash(password)
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        return my_custom_sha256_hash(password) == hashed


class UserSession:
    """
    Represents an active user session
    Demonstrates: Encapsulation with private attributes
    """
    
    def __init__(self, user_id: int, username: str, role: UserRole):
        self.__user_id: int = user_id
        self.__username: str = username
        self.__role: UserRole = role
        self.__is_active: bool = True
    
    @property
    def user_id(self) -> int:
        """Get user ID (read-only)"""
        return self.__user_id
    
    @property
    def username(self) -> str:
        """Get username (read-only)"""
        return self.__username
    
    @property
    def role(self) -> UserRole:
        """Get user role (read-only)"""
        return self.__role
    
    @property
    def is_active(self) -> bool:
        """Check if session is active"""
        return self.__is_active
    
    def has_permission(self, required_role: UserRole) -> bool:
        """Check if user has required permission level"""
        return self.__role.value >= required_role.value
    
    def can_save_builds(self) -> bool:
        """Check if user can save builds"""
        return self.__role.value >= UserRole.STANDARD.value
    
    def can_manage_users(self) -> bool:
        """Check if user can manage other users"""
        return self.__role.value >= UserRole.ADMIN.value
    
    def logout(self) -> None:
        """Deactivate session"""
        self.__is_active = False
    
    def __str__(self) -> str:
        return f"Session: {self.__username} ({self.__role.name})"


class AuthenticationService:
    """
    Authentication service with OOP design
    Demonstrates: Singleton pattern, Strategy pattern, Encapsulation
    """
    
    __instance: Optional['AuthenticationService'] = None
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton)"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        """Initialize authentication service"""
        if not hasattr(self, '_initialized'):
            self.__db_manager = get_database_manager()
            self.__hash_strategy: PasswordHashStrategy = CustomSHA256Strategy()
            self.__current_session: Optional[UserSession] = None
            self._initialized = True
    
    @property
    def current_session(self) -> Optional[UserSession]:
        """Get current active session"""
        return self.__current_session
    
    @property
    def is_authenticated(self) -> bool:
        """Check if there's an active session"""
        return self.__current_session is not None and self.__current_session.is_active
    
    def set_hash_strategy(self, strategy: PasswordHashStrategy) -> None:
        """Change hashing strategy (Strategy pattern)"""
        self.__hash_strategy = strategy
    
    def __validate_username(self, username: str) -> tuple[bool, str]:
        """Validate username format (private method)"""
        if not username:
            return False, "Username cannot be empty"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 30:
            return False, "Username must be at most 30 characters"
        if not username.replace('_', '').replace('-', '').isalnum():
            return False, "Username can only contain letters, numbers, hyphens, and underscores"
        return True, "Valid"
    
    def __validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password strength (private method)"""
        if not password:
            return False, "Password cannot be empty"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if len(password) > 100:
            return False, "Password is too long"
        return True, "Valid"
    
    def register_user(self, username: str, password: str, role: int = 1) -> tuple[bool, str]:
        """
        Register a new user
        Returns: (success, message)
        """
        # Validate username
        valid, message = self.__validate_username(username)
        if not valid:
            return False, message
        
        # Validate password
        valid, message = self.__validate_password(password)
        if not valid:
            return False, message
        
        # Attempt to create user
        try:
            user_id = self.__db_manager.create_user(username, password, role)
            if user_id is None:
                return False, "Username already exists"
            return True, f"Account created successfully (ID: {user_id})"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        Authenticate user and create session
        Returns: (success, message)
        """
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required"
        
        # Attempt authentication
        result = self.__db_manager.authenticate_user(username, password)
        if result is None:
            return False, "Invalid username or password"
        
        user_id, role_value = result
        
        # Create session
        try:
            role = UserRole(role_value)
        except ValueError:
            role = UserRole.STANDARD
        
        self.__current_session = UserSession(user_id, username, role)
        
        return True, f"Welcome, {username}!"
    
    def logout(self) -> None:
        """End current session"""
        if self.__current_session is not None:
            self.__current_session.logout()
            self.__current_session = None
    
    def require_permission(self, required_role: UserRole) -> tuple[bool, str]:
        """
        Check if current user has required permission
        Returns: (has_permission, message)
        """
        if not self.is_authenticated:
            return False, "You must be logged in"
        
        if not self.__current_session.has_permission(required_role):
            return False, f"This action requires {required_role.name} role or higher"
        
        return True, "Permission granted"
    
    def get_current_user_id(self) -> Optional[int]:
        """Get current user's ID"""
        if self.__current_session is None:
            return None
        return self.__current_session.user_id
    
    def get_current_username(self) -> Optional[str]:
        """Get current username"""
        if self.__current_session is None:
            return None
        return self.__current_session.username
    
    def get_current_role(self) -> Optional[UserRole]:
        """Get current user's role"""
        if self.__current_session is None:
            return None
        return self.__current_session.role
    
    def __str__(self) -> str:
        if self.is_authenticated:
            return f"AuthService: Logged in as {self.__current_session.username}"
        return "AuthService: No active session"


# Convenience function to get singleton instance
def get_auth_service() -> AuthenticationService:
    """Get the singleton AuthenticationService instance"""
    return AuthenticationService()
