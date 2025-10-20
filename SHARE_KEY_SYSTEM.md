# Build Share Key System

## Overview
The share key system allows users to share their PC builds with others using a unique 8-character code.

## Features

### 1. **Automatic Share Key Generation**
- When a build is saved, a unique 8-character share key is automatically generated
- Share keys use uppercase letters and digits (A-Z, 0-9) for easy sharing
- Example: `A7K9X2M1`

### 2. **Share Key Display**
After saving a build, users see:
- Success message with build name
- The unique share key in a large, readable format
- Copy button to quickly copy the key to clipboard
- Visual feedback when key is copied ("✓ Copied!")

### 3. **Import Build from Share Key**
Located at the top of the "My Builds" tab:
- **Input field**: Enter an 8-character share key
- **Import button**: Click to import the build
- Imported builds are added to your saved builds with "(imported)" suffix
- You get your own unique share key for the imported build

### 4. **Share Key in Builds List**
The builds list now displays:
- ID
- Build Name
- Created Date
- Number of Parts
- Total Price
- **Share Key** (new column)

## How to Use

### Sharing a Build:
1. Create your PC build in the Builder tab
2. Click "Save Build"
3. Enter a name for your build
4. Copy the share key shown in the success dialog
5. Share the key with friends via text, email, etc.

### Importing a Build:
1. Go to "My Builds" tab
2. Find the "Import Build from Share Key" section at the top
3. Enter the 8-character key (e.g., `A7K9X2M1`)
4. Click "Import Build"
5. The build is now in your saved builds!

## Technical Details

### Database Changes
- Added `share_key` column to `builds` table
- Added index on `share_key` for fast lookups
- Migration script: `add_share_key_column.py`

### New Functions (`pcbuilder/db.py`)
- `generate_share_key()`: Creates unique 8-character keys
- `save_build()`: Now returns `(build_id, share_key)` tuple
- `load_build_by_share_key(share_key)`: Loads build by key
- `import_build_from_share_key(user_id, share_key)`: Imports build to user's account

### Security Features
- Share keys are randomly generated using `secrets` module (cryptographically secure)
- Uniqueness is enforced (checks for duplicates before saving)
- Keys are case-insensitive (converted to uppercase)
- Invalid keys show appropriate error messages

## Benefits for NEA

This feature demonstrates:
- **Data sharing mechanisms**: Secure key-based sharing
- **Database design**: Indexed columns for performance
- **User experience**: Easy copy/paste workflow
- **Error handling**: Validates key format and existence
- **Cryptography**: Uses secure random generation
- **Collaboration features**: Social aspect of PC building

## Example Workflow

```
User A:
1. Builds high-end gaming PC (£2500)
2. Saves build → Gets key: "B4K7N9X2"
3. Shares key with User B

User B:
1. Goes to My Builds tab
2. Enters "B4K7N9X2" in Import section
3. Clicks Import Build
4. Gets copy: "High-end Gaming PC (imported)"
5. Can modify and save their own version
```

## Edge Cases Handled
- ✅ Duplicate share keys (regenerates until unique)
- ✅ Invalid key length (shows warning)
- ✅ Non-existent keys (shows error)
- ✅ Empty input (shows warning)
- ✅ Case insensitivity (auto-converts to uppercase)
- ✅ Old builds without share keys (shows "N/A")
