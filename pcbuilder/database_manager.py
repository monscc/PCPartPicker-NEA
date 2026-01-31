"""
Database Manager with Object-Oriented Design
Implements: Singleton pattern, Encapsulation, Abstraction
"""
import sqlite3
from pathlib import Path
import json
import secrets
import string
from typing import List, Optional, Dict, Any
from datetime import datetime
from threading import Lock
from .custom_hash import my_custom_sha256_hash
from .models import Component, ComponentFactory, Build


class DatabaseManager:
    """
    Singleton Database Manager
    Demonstrates: Singleton pattern, Encapsulation with private attributes
    """
    
    # Class-level attributes for singleton pattern
    __instance: Optional['DatabaseManager'] = None
    __lock: Lock = Lock()
    
    def __new__(cls, db_path: Optional[Path] = None):
        """Ensure only one instance exists (Singleton pattern)"""
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database manager"""
        # Only initialize once
        if not hasattr(self, '_initialized'):
            if db_path is None:
                db_path = Path(__file__).resolve().parent.parent / "pcbuilder.db"
            
            # Private attributes
            self.__db_path: Path = db_path
            self.__connection: Optional[sqlite3.Connection] = None
            self._initialized = True
            
            # Initialize database schema
            self.__initialize_schema()
    
    @property
    def db_path(self) -> Path:
        """Get database path (read-only)"""
        return self.__db_path
    
    def __get_connection(self) -> sqlite3.Connection:
        """Get database connection (private method)"""
        # Add timeout to handle OneDrive sync issues
        conn = sqlite3.connect(self.__db_path, timeout=30.0)
        # Enable WAL mode for better concurrent access
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    def __initialize_schema(self) -> None:
        """Initialize database schema (private method)"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        # Create parts table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS parts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                attributes TEXT
            )
        """)
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        
        # Create builds table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                parts_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                share_key TEXT UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for performance
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_parts_category 
            ON parts(category)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_builds_user 
            ON builds(user_id)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_builds_share_key 
            ON builds(share_key)
        """)
        
        conn.commit()
        conn.close()
    
    # === Component Management Methods ===
    
    def add_component(self, component: Component) -> bool:
        """Add a component to the database"""
        try:
            conn = self.__get_connection()
            cur = conn.cursor()
            
            comp_dict = component.to_dict()
            cur.execute(
                """INSERT OR REPLACE INTO parts 
                   (id, name, category, price, attributes) 
                   VALUES (?, ?, ?, ?, ?)""",
                (comp_dict['id'], comp_dict['name'], comp_dict['category'],
                 comp_dict['price'], json.dumps(comp_dict['attributes']))
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding component: {e}")
            return False
    
    def get_component_by_id(self, component_id: str) -> Optional[Component]:
        """Get a specific component by ID"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, name, category, price, attributes FROM parts WHERE id = ?",
            (component_id,)
        )
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        return ComponentFactory.create_component(
            row[0], row[1], row[2], row[3],
            json.loads(row[4]) if row[4] else {}
        )
    
    def get_all_components(self) -> List[Component]:
        """Get all components from database"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, name, category, price, attributes FROM parts")
        rows = cur.fetchall()
        conn.close()
        
        components = []
        for row in rows:
            try:
                component = ComponentFactory.create_component(
                    row[0], row[1], row[2], row[3],
                    json.loads(row[4]) if row[4] else {}
                )
                components.append(component)
            except Exception as e:
                print(f"Error loading component {row[0]}: {e}")
        
        return components
    
    def get_components_by_category(self, category: str) -> List[Component]:
        """Get all components of a specific category"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, name, category, price, attributes FROM parts WHERE category = ?",
            (category,)
        )
        rows = cur.fetchall()
        conn.close()
        
        components = []
        for row in rows:
            try:
                component = ComponentFactory.create_component(
                    row[0], row[1], row[2], row[3],
                    json.loads(row[4]) if row[4] else {}
                )
                components.append(component)
            except Exception as e:
                print(f"Error loading component {row[0]}: {e}")
        
        return components
    
    def load_components_from_json(self, json_path: Path) -> int:
        """Load components from JSON file, returns count of loaded components"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            count = 0
            for item in data:
                try:
                    component = ComponentFactory.create_component(
                        item['id'], item['name'], item['category'],
                        item['price'], item.get('attributes', {})
                    )
                    if self.add_component(component):
                        count += 1
                except Exception as e:
                    print(f"Error loading component {item.get('id', 'unknown')}: {e}")
            
            return count
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return 0
    
    # === User Management Methods ===
    
    def __hash_password(self, password: str) -> str:
        """Hash password using custom SHA256 (private method)"""
        return my_custom_sha256_hash(password)
    
    def create_user(self, username: str, password: str, role: int = 1) -> Optional[int]:
        """Create a new user account"""
        # Validation
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        try:
            conn = self.__get_connection()
            cur = conn.cursor()
            
            password_hash = self.__hash_password(password)
            cur.execute(
                """INSERT INTO users (username, password_hash, role, created_at) 
                   VALUES (?, ?, ?, ?)""",
                (username, password_hash, role, datetime.now().isoformat())
            )
            
            user_id = cur.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None  # Username already exists
    
    def authenticate_user(self, username: str, password: str) -> Optional[tuple[int, int]]:
        """Authenticate user and return (user_id, role)"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, password_hash, role FROM users WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        user_id, stored_hash, role = row
        if self.__hash_password(password) == stored_hash:
            return (user_id, role)
        
        return None
    
    def get_user_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user information"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, username, role, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        return {
            'id': row[0],
            'username': row[1],
            'role': row[2],
            'created_at': row[3]
        }
    
    # === Build Management Methods ===
    
    def __generate_share_key(self) -> str:
        """Generate unique share key (private method)"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(8))
    
    def save_build(self, build: Build) -> tuple[int, str]:
        """Save a build to database, returns (build_id, share_key)"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        # Generate unique share key
        share_key = self.__generate_share_key()
        while True:
            cur.execute("SELECT id FROM builds WHERE share_key = ?", (share_key,))
            if cur.fetchone() is None:
                break
            share_key = self.__generate_share_key()
        
        build.share_key = share_key
        
        # Serialize components
        parts_dict = {}
        for category, component in build.get_all_components().items():
            if component is not None:
                parts_dict[category] = component.to_dict()
            else:
                parts_dict[category] = None
        
        cur.execute(
            """INSERT INTO builds (user_id, name, parts_json, created_at, share_key)
               VALUES (?, ?, ?, ?, ?)""",
            (build.user_id, build.name, json.dumps(parts_dict),
             datetime.now().isoformat(), share_key)
        )
        
        build_id = cur.lastrowid
        build.build_id = build_id
        
        conn.commit()
        conn.close()
        
        return (build_id, share_key)
    
    def load_build(self, build_id: int) -> Optional[Build]:
        """Load a build by ID"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            """SELECT id, user_id, name, parts_json, created_at, share_key 
               FROM builds WHERE id = ?""",
            (build_id,)
        )
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        return self.__build_from_row(row)
    
    def load_build_by_share_key(self, share_key: str) -> Optional[Build]:
        """Load a build by share key"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            """SELECT id, user_id, name, parts_json, created_at, share_key 
               FROM builds WHERE share_key = ?""",
            (share_key,)
        )
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        return self.__build_from_row(row)
    
    def load_user_builds(self, user_id: int) -> List[Build]:
        """Load all builds for a user"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        cur.execute(
            """SELECT id, user_id, name, parts_json, created_at, share_key 
               FROM builds WHERE user_id = ?""",
            (user_id,)
        )
        rows = cur.fetchall()
        conn.close()
        
        builds = []
        for row in rows:
            try:
                build = self.__build_from_row(row)
                if build:
                    builds.append(build)
            except Exception as e:
                print(f"Error loading build {row[0]}: {e}")
        
        return builds
    
    def __build_from_row(self, row: tuple) -> Optional[Build]:
        """Convert database row to Build object (private method)"""
        try:
            build_id, user_id, name, parts_json, created_at, share_key = row
            
            build = Build(build_id, name, user_id)
            build.share_key = share_key
            
            # Deserialize components
            parts_dict = json.loads(parts_json)
            for category, comp_data in parts_dict.items():
                if comp_data is not None:
                    component = ComponentFactory.create_component(
                        comp_data['id'], comp_data['name'], comp_data['category'],
                        comp_data['price'], comp_data.get('attributes', {})
                    )
                    build.add_component(component)
            
            return build
        except Exception as e:
            print(f"Error building from row: {e}")
            return None
    
    def import_build(self, user_id: int, share_key: str) -> Optional[tuple[int, str]]:
        """Import a build from share key to user's account"""
        build = self.load_build_by_share_key(share_key)
        if build is None:
            return None
        
        # Create a copy for the new user
        new_build = Build(None, f"{build.name} (imported)", user_id)
        for category, component in build.get_all_components().items():
            if component is not None:
                new_build.add_component(component)
        
        return self.save_build(new_build)
    
    def delete_build(self, build_id: int, user_id: int) -> bool:
        """Delete a build (only if owned by user)"""
        try:
            conn = self.__get_connection()
            cur = conn.cursor()
            
            cur.execute(
                "DELETE FROM builds WHERE id = ? AND user_id = ?",
                (build_id, user_id)
            )
            
            deleted = cur.rowcount > 0
            conn.commit()
            conn.close()
            return deleted
        except Exception as e:
            print(f"Error deleting build: {e}")
            return False
    
    # === Utility Methods ===
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.__get_connection()
        cur = conn.cursor()
        
        # Count components by category
        cur.execute("""
            SELECT category, COUNT(*) 
            FROM parts 
            GROUP BY category
        """)
        components_by_category = dict(cur.fetchall())
        
        # Count total users
        cur.execute("SELECT COUNT(*) FROM users")
        total_users = cur.fetchone()[0]
        
        # Count total builds
        cur.execute("SELECT COUNT(*) FROM builds")
        total_builds = cur.fetchone()[0]
        
        conn.close()
        
        return {
            'components_by_category': components_by_category,
            'total_users': total_users,
            'total_builds': total_builds
        }
    
    def close(self) -> None:
        """Close database connection (if needed)"""
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None


# Convenience function to get singleton instance
def get_database_manager() -> DatabaseManager:
    """Get the singleton DatabaseManager instance"""
    return DatabaseManager()
