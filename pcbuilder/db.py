"""
Database module - Backward compatibility layer
Provides procedural interface to new OOP DatabaseManager
"""
import sqlite3
from pathlib import Path
import json
from typing import List, Optional, Dict
from datetime import datetime
from .database_manager import get_database_manager
from .custom_hash import my_custom_sha256_hash


DB_FILE = Path(__file__).resolve().parent.parent / "pcbuilder.db"

# Get singleton database manager instance
_db_manager = get_database_manager()


def init_db(db_path: Path = DB_FILE):
    """Initialize database (handled automatically by DatabaseManager)"""
    pass  # DatabaseManager handles initialization


def load_sample_parts(json_path: Path) -> None:
    """Load components from JSON file"""
    _db_manager.load_components_from_json(json_path)


def list_parts() -> List[dict]:
    """Get all components as dictionaries"""
    components = _db_manager.get_all_components()
    return [comp.to_dict() for comp in components]


def hash_password(password: str) -> str:
    """Hash password using custom SHA256"""
    return my_custom_sha256_hash(password)


def create_user(username: str, password: str, role: int = 1) -> Optional[int]:
    """Create a new user account"""
    try:
        return _db_manager.create_user(username, password, role)
    except ValueError:
        return None


def login_user(username: str, password: str) -> Optional[tuple]:
    """Verify credentials"""
    return _db_manager.authenticate_user(username, password)


def generate_share_key() -> str:
    """Generate a unique share key"""
    import secrets
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))


def save_build(user_id: int, build_name: str, parts: Dict[str, Optional[Dict]]) -> tuple:
    """Save a build for a user"""
    from .models import Build, ComponentFactory
    
    # Create Build object from parts dict
    build = Build(None, build_name, user_id)
    
    for category, part_dict in parts.items():
        if part_dict is not None:
            component = ComponentFactory.create_component(
                part_dict['id'], part_dict['name'], part_dict['category'],
                part_dict['price'], part_dict.get('attributes', {})
            )
            build.add_component(component)
    
    return _db_manager.save_build(build)


def load_user_builds(user_id: int) -> List[Dict]:
    """Load all builds for a user"""
    builds = _db_manager.load_user_builds(user_id)
    return [build.to_dict() for build in builds]


def load_build_by_id(build_id: int) -> Optional[Dict]:
    """Load a specific build by ID"""
    build = _db_manager.load_build(build_id)
    if build is None:
        return None
    return build.to_dict()


def load_build_by_share_key(share_key: str) -> Optional[Dict]:
    """Load a build by its share key"""
    build = _db_manager.load_build_by_share_key(share_key)
    if build is None:
        return None
    return build.to_dict()


def import_build_from_share_key(user_id: int, share_key: str) -> Optional[tuple]:
    """Import a build from a share key"""
    return _db_manager.import_build(user_id, share_key)

