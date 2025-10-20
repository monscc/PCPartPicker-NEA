import sqlite3

print("Attempting to add role column to users table...")

try:
    conn = sqlite3.connect('pcbuilder.db')
    cur = conn.cursor()
    
    # Check current schema
    cur.execute('PRAGMA table_info(users)')
    columns = cur.fetchall()
    print("\nCurrent table schema:")
    for col in columns:
        print(f"  {col}")
    
    # Check if role column exists
    column_names = [col[1] for col in columns]
    
    if 'role' not in column_names:
        print("\nRole column not found. Adding it now...")
        cur.execute('ALTER TABLE users ADD COLUMN role INTEGER DEFAULT 1')
        conn.commit()
        print("✅ Role column added successfully!")
    else:
        print("\n✅ Role column already exists!")
    
    # Verify
    cur.execute('PRAGMA table_info(users)')
    columns = cur.fetchall()
    print("\nUpdated table schema:")
    for col in columns:
        print(f"  {col}")
    
    conn.close()
    print("\nMigration complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
