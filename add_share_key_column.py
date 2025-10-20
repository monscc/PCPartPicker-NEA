"""
Migration script to add share_key column to builds table
"""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "pcbuilder.db"

def add_share_key_column():
    """Add share_key column to builds table"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Check if column already exists
    cur.execute("PRAGMA table_info(builds)")
    columns = [column[1] for column in cur.fetchall()]
    
    if 'share_key' not in columns:
        print("Adding share_key column to builds table...")
        # Add column without UNIQUE constraint (can't add UNIQUE in ALTER TABLE)
        cur.execute("ALTER TABLE builds ADD COLUMN share_key TEXT")
        conn.commit()
        
        # Create index for faster lookups
        cur.execute("CREATE INDEX IF NOT EXISTS idx_share_key ON builds(share_key)")
        conn.commit()
        print("✅ Column added successfully!")
    else:
        print("ℹ️  share_key column already exists")
    
    conn.close()

if __name__ == "__main__":
    add_share_key_column()
