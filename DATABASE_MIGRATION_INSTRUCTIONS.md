# Database Migration Instructions

## Problem
The database was created before the `role` column was added to the `users` table, causing login/registration failures.

## Solution: Add the Role Column

### Option 1: Run Migration Script (Recommended)
1. **Close the GUI if it's running** (Press Ctrl+C in the terminal)
2. Run the migration script:
   ```powershell
   python add_role_column.py
   ```
3. You should see output confirming the column was added
4. Restart the GUI:
   ```powershell
   python run_gui.py
   ```

### Option 2: Manual SQL (If script fails)
1. Close the GUI
2. Open Python and run these commands:
   ```python
   import sqlite3
   conn = sqlite3.connect('pcbuilder.db')
   cur = conn.cursor()
   cur.execute('ALTER TABLE users ADD COLUMN role INTEGER DEFAULT 1')
   conn.commit()
   conn.close()
   print("Done!")
   ```

### Option 3: Delete and Recreate Database
If the above options don't work:

1. Close the GUI
2. Delete the database file:
   ```powershell
   Remove-Item pcbuilder.db
   ```
3. Restart the GUI - it will create a new database with the correct schema:
   ```powershell
   python run_gui.py
   ```
4. Note: This will delete any existing users and builds!

## Verification

After running the migration, verify it worked:

```python
import sqlite3
conn = sqlite3.connect('pcbuilder.db')
cur = conn.cursor()
cur.execute('PRAGMA table_info(users)')
for col in cur.fetchall():
    print(col)
conn.close()
```

You should see a column named 'role' in the output.

## Expected Table Schema

```
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'username', 'TEXT', 1, None, 0)
(2, 'password_hash', 'TEXT', 1, None, 0)
(3, 'created_at', 'TEXT', 0, None, 0)
(4, 'role', 'INTEGER', 0, '1', 0)  ← This should exist
```

## What the Migration Does

1. Checks if the 'role' column exists in the users table
2. If not, adds it with default value of 1 (STANDARD role)
3. Sets all existing users to STANDARD role
4. Commits the changes

## Role Values

- 0 = GUEST
- 1 = STANDARD (default for registered users)
- 2 = PREMIUM
- 3 = ADMIN
