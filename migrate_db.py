"""
Database Migration Script
Adds role column to existing users table
"""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "pcbuilder.db"


def migrate_database():
    """Add role column to users table if it doesn't exist"""
    print("Starting database migration...")
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    try:
        # Check if role column exists
        cur.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cur.fetchall()]
        
        if 'role' not in columns:
            print("Adding 'role' column to users table...")
            
            # Add role column with default value of 1 (STANDARD)
            cur.execute("ALTER TABLE users ADD COLUMN role INTEGER DEFAULT 1")
            
            # Update all existing users to STANDARD role
            cur.execute("UPDATE users SET role = 1 WHERE role IS NULL")
            
            conn.commit()
            print("✅ Migration successful! Role column added.")
            print("   All existing users have been set to STANDARD role (1)")
        else:
            print("✅ Role column already exists. No migration needed.")
        
        # Verify the migration
        cur.execute("PRAGMA table_info(users)")
        print("\nCurrent users table structure:")
        for column in cur.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        # Show user count
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        print(f"\nTotal users in database: {user_count}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_database()
