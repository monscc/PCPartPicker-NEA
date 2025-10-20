# Object-Oriented Programming Implementation

## Overview
The PC Part Picker application has been refactored to implement comprehensive Object-Oriented Programming (OOP) principles, demonstrating advanced programming skills suitable for A-Level Computer Science NEA requirements.

## OOP Principles Implemented

### 1. **Abstraction**
Abstract base classes define interfaces without implementation details:

#### Component (Abstract Base Class)
```python
class Component(ABC):
    @abstractmethod
    def get_category(self) -> ComponentCategory:
        """Each component must define its category"""
        pass
    
    @abstractmethod
    def is_compatible_with(self, other: 'Component') -> tuple[bool, str]:
        """Check compatibility with another component"""
        pass
    
    @abstractmethod
    def get_specifications(self) -> Dict[str, Any]:
        """Get formatted specifications"""
        pass
```

**Benefits:**
- Enforces consistent interface across all component types
- Cannot instantiate abstract class directly
- Guarantees all subclasses implement required methods

### 2. **Encapsulation**
Private attributes with controlled access via properties:

#### Example from Component Class
```python
class Component(ABC):
    def __init__(self, component_id: str, name: str, price: float, attributes: Dict):
        # Private attributes using name mangling
        self.__id: str = component_id
        self.__name: str = name
        self.__price: float = price
        self.__attributes: Dict[str, Any] = attributes
    
    @property
    def id(self) -> str:
        """Get component ID (read-only)"""
        return self.__id
    
    @property
    def price(self) -> float:
        """Get component price"""
        return self.__price
    
    @price.setter
    def price(self, value: float) -> None:
        """Set component price with validation"""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value
```

**Benefits:**
- Data protection: Cannot access `__id` directly
- Validation: Price setter ensures no negative values
- Read-only properties: ID cannot be changed after creation
- Controlled access: All attribute access goes through properties

### 3. **Inheritance**
Concrete classes inherit from abstract base:

#### Component Hierarchy
```
Component (ABC)
├── CPU
├── GPU
├── Motherboard
├── RAM
├── Storage
├── PSU
├── Case
└── Cooler
```

**Example Implementation:**
```python
class CPU(Component):
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.CPU
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        if isinstance(other, Motherboard):
            cpu_socket = self.get_attribute('socket', '')
            mb_socket = other.get_attribute('socket', '')
            if cpu_socket == mb_socket:
                return True, "Compatible sockets"
            return False, f"Incompatible sockets"
        return True, "No constraints"
    
    def get_specifications(self) -> Dict[str, Any]:
        return {
            'Cores': self.get_attribute('cores', 'N/A'),
            'Socket': self.get_attribute('socket', 'N/A'),
            'TDP': f"{self.get_attribute('tdp', 'N/A')} W"
        }
```

### 4. **Polymorphism**
Different component types respond differently to same method calls:

```python
# All components can check compatibility, but logic differs
cpu.is_compatible_with(motherboard)  # Checks socket match
gpu.is_compatible_with(psu)          # Checks power requirements
case.is_compatible_with(motherboard) # Checks form factor
```

### 5. **Singleton Pattern**
Ensures only one instance of critical services:

```python
class DatabaseManager:
    __instance: Optional['DatabaseManager'] = None
    __lock: Lock = Lock()
    
    def __new__(cls, db_path: Optional[Path] = None):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance
```

**Benefits:**
- Single database connection
- Shared state across application
- Thread-safe initialization
- Prevents resource conflicts

### 6. **Factory Pattern**
Creates appropriate component instances:

```python
class ComponentFactory:
    _component_map = {
        'CPU': CPU,
        'Motherboard': Motherboard,
        'GPU': GPU,
        # ...
    }
    
    @classmethod
    def create_component(cls, component_id: str, name: str, category: str,
                        price: float, attributes: Dict[str, Any]) -> Component:
        component_class = cls._component_map.get(category)
        if component_class is None:
            raise ValueError(f"Unknown category: {category}")
        return component_class(component_id, name, price, attributes)
```

**Benefits:**
- Centralized object creation
- Easy to add new component types
- Type safety (returns appropriate subclass)
- Decouples creation from usage

### 7. **Strategy Pattern**
Interchangeable algorithms for password hashing:

```python
class PasswordHashStrategy(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed: str) -> bool:
        pass

class CustomSHA256Strategy(PasswordHashStrategy):
    def hash_password(self, password: str) -> str:
        return my_custom_sha256_hash(password)
    
    def verify_password(self, password: str, hashed: str) -> bool:
        return my_custom_sha256_hash(password) == hashed

# Can switch strategies at runtime
auth_service.set_hash_strategy(CustomSHA256Strategy())
```

### 8. **Composition**
Build class contains Component objects:

```python
class Build:
    def __init__(self, build_id: Optional[int], name: str, user_id: int):
        self.__components: Dict[str, Optional[Component]] = {
            'CPU': None,
            'Motherboard': None,
            # ...
        }
    
    def add_component(self, component: Component) -> None:
        category = component.get_category().value
        self.__components[category] = component
```

**Benefits:**
- Build "has-a" Component (composition)
- Not inheritance (Build is not a Component)
- More flexible than inheritance
- Components can be added/removed dynamically

## Class Structure

### Core Classes

#### 1. Component (Abstract Base Class)
**File:** `pcbuilder/models.py`

**Purpose:** Define interface for all PC components

**Private Attributes:**
- `__id`: Component unique identifier
- `__name`: Component name
- `__price`: Component price (with validation)
- `__attributes`: Component specifications

**Public Methods:**
- `get_category()`: Returns component category
- `is_compatible_with()`: Check compatibility with another component
- `get_specifications()`: Get formatted specifications
- `to_dict()`: Serialize to dictionary

**Concrete Subclasses:**
- CPU, GPU, Motherboard, RAM, Storage, PSU, Case, Cooler

#### 2. Build
**File:** `pcbuilder/models.py`

**Purpose:** Manage a PC build with multiple components

**Private Attributes:**
- `__build_id`: Build database ID
- `__name`: Build name (min 3 characters)
- `__user_id`: Owner user ID
- `__components`: Dictionary of components
- `__share_key`: Unique share key

**Public Methods:**
- `add_component()`: Add component to build
- `remove_component()`: Remove component from build
- `get_component()`: Get specific component
- `calculate_total_price()`: Sum all component prices
- `calculate_total_wattage()`: Sum power consumption
- `is_complete()`: Check if all essential parts present
- `get_compatibility_issues()`: List compatibility problems

#### 3. DatabaseManager (Singleton)
**File:** `pcbuilder/database_manager.py`

**Purpose:** Centralized database operations

**Private Attributes:**
- `__db_path`: Database file path
- `__connection`: SQLite connection

**Private Methods:**
- `__get_connection()`: Get database connection
- `__initialize_schema()`: Create tables
- `__hash_password()`: Hash password
- `__generate_share_key()`: Generate unique key
- `__build_from_row()`: Deserialize build

**Public Methods:**
- `add_component()`: Add component to database
- `get_component_by_id()`: Retrieve specific component
- `get_all_components()`: Get all components
- `create_user()`: Register new user
- `authenticate_user()`: Verify credentials
- `save_build()`: Persist build
- `load_build()`: Retrieve build

#### 4. AuthenticationService (Singleton)
**File:** `pcbuilder/auth_service.py`

**Purpose:** User authentication and session management

**Private Attributes:**
- `__db_manager`: Database manager instance
- `__hash_strategy`: Password hashing strategy
- `__current_session`: Active user session

**Private Methods:**
- `__validate_username()`: Check username requirements
- `__validate_password()`: Check password strength

**Public Methods:**
- `register_user()`: Create new account
- `login()`: Authenticate and create session
- `logout()`: End session
- `require_permission()`: Check user permissions
- `get_current_user_id()`: Get logged-in user ID

#### 5. UserSession
**File:** `pcbuilder/auth_service.py`

**Purpose:** Represent active user session

**Private Attributes:**
- `__user_id`: User ID
- `__username`: Username
- `__role`: User role level
- `__is_active`: Session status

**Public Methods:**
- `has_permission()`: Check role level
- `can_save_builds()`: Check save permission
- `logout()`: Deactivate session

## Access Modifiers

### Private Attributes (Name Mangling)
```python
class Component:
    def __init__(self):
        self.__id = "private"     # Cannot access directly
        self._protected = "prot"  # Convention: internal use
        self.public = "public"     # Accessible anywhere
```

**Testing:**
```python
cpu = CPU(...)
cpu.id        # ✓ Works (through property)
cpu.__id      # ✗ AttributeError
cpu._Component__id  # ✓ Works (name mangling)
```

### Property Decorators
```python
@property
def price(self) -> float:
    """Getter - read access"""
    return self.__price

@price.setter
def price(self, value: float) -> None:
    """Setter - write access with validation"""
    if value < 0:
        raise ValueError("Price cannot be negative")
    self.__price = value
```

## Design Patterns Summary

| Pattern | Class | Purpose |
|---------|-------|---------|
| **Singleton** | DatabaseManager | Single database instance |
| **Singleton** | AuthenticationService | Single auth service |
| **Factory** | ComponentFactory | Create component instances |
| **Strategy** | PasswordHashStrategy | Interchangeable hashing |
| **Abstract Factory** | Component (ABC) | Component interface |
| **Composition** | Build contains Components | Has-a relationship |
| **Template Method** | Component.to_dict() | Serialization pattern |

## Backward Compatibility

The OOP refactoring maintains backward compatibility through adapter layers:

### db.py (Procedural → OOP Adapter)
```python
# Old procedural interface
_db_manager = get_database_manager()

def list_parts() -> List[dict]:
    """Procedural wrapper"""
    components = _db_manager.get_all_components()
    return [comp.to_dict() for comp in components]
```

**Benefits:**
- Existing code continues to work
- Gradual migration possible
- No breaking changes
- Clean separation of concerns

## Key Benefits

### 1. **Maintainability**
- Changes to Component affect all subclasses
- Single Responsibility: Each class has one job
- Open/Closed: Open for extension, closed for modification

### 2. **Testability**
- Mock components easily
- Test classes in isolation
- Strategy pattern allows test doubles

### 3. **Extensibility**
- Add new component types by inheriting Component
- Add new hash strategies by inheriting PasswordHashStrategy
- Factory pattern makes adding types trivial

### 4. **Code Reuse**
- Common functionality in base classes
- DRY principle (Don't Repeat Yourself)
- Shared methods through inheritance

### 5. **Type Safety**
- Strong typing with type hints
- Factory ensures correct types
- Properties enforce validation

## NEA Compliance

This implementation demonstrates A-Level CS required skills:

✅ **Abstract Data Types** - Component, User, Build  
✅ **Encapsulation** - Private attributes with name mangling  
✅ **Inheritance** - Component → CPU, GPU, etc.  
✅ **Polymorphism** - is_compatible_with() behaves differently  
✅ **Composition** - Build contains Components  
✅ **Design Patterns** - Singleton, Factory, Strategy  
✅ **Access Modifiers** - Private (__), Protected (_), Public  
✅ **Properties** - @property decorators  
✅ **Type Hints** - All methods typed  
✅ **Exception Handling** - Validation with exceptions  
✅ **Documentation** - Comprehensive docstrings  

## File Structure

```
pcbuilder/
├── models.py              # Core OOP models (Component, Build, etc.)
├── database_manager.py    # DatabaseManager singleton
├── auth_service.py        # AuthenticationService singleton
├── db.py                  # Backward compatibility layer
├── accounts.py            # Account management wrapper
└── custom_hash.py         # Custom SHA256 implementation
```

## Example Usage

### Creating Components (Factory Pattern)
```python
from pcbuilder.models import ComponentFactory

cpu = ComponentFactory.create_component(
    'cpu_001', 'Intel i7-12700K', 'CPU', 329.99,
    {'cores': 12, 'socket': 'LGA1700', 'tdp': 125}
)
# Returns CPU instance (not generic Component)
```

### Building a PC (Composition)
```python
from pcbuilder.models import Build

build = Build(None, "Gaming Build", user_id=1)
build.add_component(cpu)
build.add_component(motherboard)
build.add_component(ram)

total = build.calculate_total_price()
issues = build.get_compatibility_issues()
```

### Using Database (Singleton)
```python
from pcbuilder.database_manager import get_database_manager

db = get_database_manager()  # Always same instance
db.add_component(cpu)
components = db.get_components_by_category('CPU')
```

### Authentication (Strategy + Singleton)
```python
from pcbuilder.auth_service import get_auth_service

auth = get_auth_service()
success, msg = auth.register_user("john", "pass123")
success, msg = auth.login("john", "pass123")

if auth.is_authenticated:
    print(f"Logged in as {auth.get_current_username()}")
```

## Conclusion

This OOP implementation demonstrates professional-grade software architecture suitable for university-level evaluation. The code exhibits:

- **Strong encapsulation** with private attributes
- **Proper abstraction** through abstract base classes
- **Flexible design** through composition and patterns
- **Production quality** with validation and error handling
- **Maintainability** through separation of concerns
- **Extensibility** through inheritance and factories

All original functionality is preserved through backward-compatible adapters while the new OOP structure provides a solid foundation for future development.
