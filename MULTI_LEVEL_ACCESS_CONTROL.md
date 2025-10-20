## Multi-Level User Access Control System

### Overview
This PC Part Picker application implements a sophisticated **Role-Based Access Control (RBAC)** system with four hierarchical user levels. This demonstrates advanced programming techniques including:

- **Enum-based role hierarchy**
- **Permission registry pattern** (Singleton)
- **Decorator-based authorization**
- **Session management**
- **Defensive programming with permission checks**

---

### User Roles

#### 1. Guest (Level 0) 🔓
**Access Rights:**
- ✅ View all components
- ✅ Build PC configurations
- ✅ Run compatibility checks
- ✅ View beginner's guide
- ❌ Save builds to database
- ❌ Load saved builds
- ❌ Track price history

**Use Case:** New users who want to explore the app without creating an account

#### 2. Standard (Level 1) 👤
**Access Rights:**
- ✅ All Guest permissions
- ✅ **Save builds** to database
- ✅ **Load saved builds**
- ✅ **Delete builds**
- ❌ Track price history
- ❌ Manage database

**Use Case:** Regular users who want to save and manage their PC builds

#### 3. Premium (Level 2) ⭐
**Access Rights:**
- ✅ All Standard permissions
- ✅ **Track price history** of components
- ✅ Receive price alerts
- ❌ Manage database

**Use Case:** Power users who want price tracking features (future implementation)

#### 4. Admin (Level 3) 🔑
**Access Rights:**
- ✅ All Premium permissions
- ✅ **Add/edit/delete** components
- ✅ **Manage user accounts**
- ✅ View system statistics

**Use Case:** System administrators (future implementation)

---

### Technical Implementation

#### 1. Permission System (`pcbuilder/auth.py`)

**Permission Registry (Singleton Pattern):**
```python
class PermissionRegistry:
    _instance = None  # Ensures only one registry exists
    
    def check(self, permission_name: str, user_role: UserRole) -> bool:
        """Verify if a role has a specific permission"""
```

**Defined Permissions:**
- `VIEW_PARTS` - View component catalog (Guest+)
- `BUILD_PC` - Create PC builds (Guest+)
- `CHECK_COMPATIBILITY` - Run compatibility checks (Guest+)
- `SAVE_BUILD` - Save builds to database (Standard+)
- `LOAD_BUILD` - Load saved builds (Standard+)
- `TRACK_PRICES` - Price history tracking (Premium+)
- `MANAGE_DATABASE` - Component management (Admin only)
- `MANAGE_USERS` - User management (Admin only)

#### 2. Authorization Decorators

**Permission-based decorator:**
```python
@requires_permission('SAVE_BUILD')
def save_build(self, build_data):
    # Only executes if user has SAVE_BUILD permission
    # Automatically raises PermissionError if unauthorized
```

**Role-based decorator:**
```python
@requires_role(UserRole.STANDARD)
def premium_feature(self):
    # Only executes if user is STANDARD or higher
```

#### 3. Session Management

**SessionManager (Singleton):**
```python
session = SessionManager()

# Guest login
session.login_guest()

# User login
session.login_user(user_id=1, username="john", role=UserRole.STANDARD)

# Check current user
current_user = session.get_current_user()
if current_user.can_save():
    # User can save builds
```

#### 4. Database Integration

**Users table schema:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role INTEGER DEFAULT 1,  -- 0=Guest, 1=Standard, 2=Premium, 3=Admin
    created_at TEXT
)
```

#### 5. UI Integration

**Login Screen:**
- Username/password fields
- Login button (creates Standard user)
- Register button (creates Standard user)
- **"Continue as Guest" button** (bypasses authentication)
- Visual indicators for guest mode

**Main Interface:**
- Role indicator badge (🔓 Guest, 👤 Standard, ⭐ Premium, 🔑 Admin)
- Username display
- Disabled "My Builds" tab for guests
- Disabled "Save Build" button for guests with tooltip

**Permission Enforcement:**
```python
# Builder tab checks permission before saving
current_user = session.get_current_user()
if not current_user or not current_user.can_save():
    messagebox.showwarning("Permission Denied", 
        "You must be signed in to save builds...")
    return
```

---

### Key Programming Techniques (NEA Marks)

#### 1. **Object-Oriented Design**
- `User` class with role-based methods
- `GuestUser` singleton subclass
- `Permission` dataclass
- Encapsulation of authorization logic

#### 2. **Design Patterns**
- **Singleton Pattern**: PermissionRegistry, SessionManager, GuestUser
- **Decorator Pattern**: @requires_permission, @requires_role
- **Strategy Pattern**: Different permission checking strategies per role

#### 3. **Defensive Programming**
- Permission checks before sensitive operations
- Graceful degradation for guest users
- Clear error messages for unauthorized access
- Type hints and docstrings throughout

#### 4. **Enum for Type Safety**
```python
class UserRole(Enum):
    GUEST = 0
    STANDARD = 1
    PREMIUM = 2
    ADMIN = 3
    
    def __lt__(self, other):
        """Enable role comparison: if role < UserRole.ADMIN"""
```

#### 5. **Functional Programming**
- Higher-order functions (decorators)
- Lambda functions in permission checks
- List comprehensions for filtering permissions

#### 6. **Data Structures**
- Dictionary-based permission registry
- Hierarchical role enumeration
- Dataclasses for structured data

---

### User Flow Examples

#### Guest User Journey:
1. Opens app → Login screen
2. Clicks "Continue as Guest" 🔓
3. Sees welcome message about guest limitations
4. Can build PC and check compatibility
5. Clicks "Save Build" → Permission denied message with suggestion to create account
6. "My Builds" tab is disabled

#### Standard User Journey:
1. Opens app → Login screen
2. Clicks "Register" → Creates account (role=STANDARD)
3. Logs in with credentials
4. Sees "👤 Standard" role indicator
5. Builds PC configuration
6. Clicks "Save Build" → Success! ✅
7. Can view/load/delete saved builds in "My Builds" tab

---

### Security Considerations

1. **Password Hashing**: SHA256 (production would use bcrypt)
2. **SQL Injection Protection**: Parameterized queries
3. **Session Validation**: Checks current_user before operations
4. **Role Verification**: Validates role level for each protected action
5. **Guest Isolation**: Guest users (user_id=None) cannot access database writes

---

### Future Enhancements

1. **Premium Features:**
   - Price history charts
   - Email price alerts
   - Build comparison tool

2. **Admin Panel:**
   - Component CRUD operations
   - User management interface
   - System analytics dashboard

3. **Enhanced Security:**
   - bcrypt password hashing
   - Session tokens
   - Two-factor authentication
   - Account recovery

4. **Granular Permissions:**
   - Custom permission sets
   - User groups
   - Temporary permission grants

---

### Testing the System

**Test Guest Access:**
1. Click "Continue as Guest"
2. Try to save a build → Should show permission denied
3. Check "My Builds" tab → Should be disabled

**Test Standard User:**
1. Register new account
2. Build PC
3. Save build → Should succeed
4. Load build → Should succeed

**Test Role Indicator:**
- Guest: 🔓 Guest
- Standard: 👤 Standard
- Premium: ⭐ Premium (when implemented)
- Admin: 🔑 Admin (when implemented)

---

This implementation demonstrates industry-standard access control patterns while remaining appropriate for an A-Level NEA project. The system is extensible, maintainable, and showcases advanced programming skills.
