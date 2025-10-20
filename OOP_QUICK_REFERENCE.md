# OOP Quick Reference Guide

## Core OOP Concepts Implemented

### 1. Classes and Objects
```python
# Class definition
class Component(ABC):
    def __init__(self, component_id, name, price, attributes):
        self.__id = component_id  # Private attribute
        
# Object instantiation
cpu = CPU('cpu_001', 'Intel i7', 329.99, {...})
```

### 2. Encapsulation (Private Attributes)
```python
class Component:
    def __init__(self):
        self.__id = "hidden"        # Private (name mangling)
        self._internal = "semi"     # Protected (convention)
        self.public = "visible"     # Public
    
    @property
    def id(self):
        """Controlled access to private attribute"""
        return self.__id
```

### 3. Inheritance
```python
# Base class
class Component(ABC):
    def calculate_value(self):
        return self.price * 0.9

# Derived class
class CPU(Component):
    def get_category(self):
        return ComponentCategory.CPU
```

### 4. Polymorphism
```python
# Same method, different behavior
components = [cpu, gpu, ram]
for comp in components:
    comp.is_compatible_with(motherboard)  # Different logic for each
```

### 5. Abstraction
```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def get_category(self):
        """Must be implemented by subclasses"""
        pass
```

### 6. Composition
```python
class Build:
    def __init__(self):
        self.__components = {}  # Build HAS components
    
    def add_component(self, component: Component):
        self.__components[component.get_category()] = component
```

## Design Patterns

### Singleton Pattern
```python
class DatabaseManager:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

# Usage
db1 = DatabaseManager()
db2 = DatabaseManager()
print(db1 is db2)  # True - same instance
```

### Factory Pattern
```python
class ComponentFactory:
    @classmethod
    def create_component(cls, category, ...):
        component_map = {
            'CPU': CPU,
            'GPU': GPU
        }
        return component_map[category](...)

# Usage
cpu = ComponentFactory.create_component('CPU', ...)
```

### Strategy Pattern
```python
class PasswordHashStrategy(ABC):
    @abstractmethod
    def hash_password(self, password):
        pass

class CustomSHA256Strategy(PasswordHashStrategy):
    def hash_password(self, password):
        return my_custom_sha256_hash(password)

# Usage
auth.set_hash_strategy(CustomSHA256Strategy())
```

## Property Decorators

### Read-Only Property
```python
@property
def id(self):
    """Cannot be modified after creation"""
    return self.__id
```

### Read-Write Property with Validation
```python
@property
def price(self):
    return self.__price

@price.setter
def price(self, value):
    if value < 0:
        raise ValueError("Price cannot be negative")
    self.__price = value
```

## Type Hints
```python
from typing import Optional, List, Dict, Any

def get_component(self, component_id: str) -> Optional[Component]:
    """Returns Component or None"""
    pass

def get_all_components(self) -> List[Component]:
    """Returns list of Components"""
    pass

def save_build(self, build: Build) -> tuple[int, str]:
    """Returns tuple of (build_id, share_key)"""
    pass
```

## Access Levels

| Modifier | Syntax | Access |
|----------|--------|--------|
| Public | `self.attribute` | Everywhere |
| Protected | `self._attribute` | Convention: internal use |
| Private | `self.__attribute` | Only within class (name mangled) |

## Example: Complete Class with All Features

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class Component(ABC):
    """
    Abstract base class demonstrating:
    - Abstraction (ABC)
    - Encapsulation (private attributes)
    - Properties
    - Type hints
    """
    
    def __init__(self, component_id: str, name: str, price: float, 
                 attributes: Dict[str, Any]):
        # Private attributes (encapsulation)
        self.__id: str = component_id
        self.__name: str = name
        self.__price: float = price
        self.__attributes: Dict[str, Any] = attributes
    
    # Property decorators (controlled access)
    @property
    def id(self) -> str:
        """Read-only property"""
        return self.__id
    
    @property
    def price(self) -> float:
        """Read-write property with validation"""
        return self.__price
    
    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value
    
    # Abstract methods (must be implemented by subclasses)
    @abstractmethod
    def get_category(self) -> str:
        """Abstract method - no implementation"""
        pass
    
    @abstractmethod
    def is_compatible_with(self, other: 'Component') -> tuple[bool, str]:
        """Polymorphic method - different for each subclass"""
        pass
    
    # Regular method
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.__id,
            'name': self.__name,
            'price': self.__price,
            'attributes': self.__attributes
        }
    
    # Special methods
    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}: {self.__name}"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"{self.__class__.__name__}(id='{self.__id}')"


class CPU(Component):
    """
    Concrete implementation demonstrating:
    - Inheritance (extends Component)
    - Method overriding (implements abstract methods)
    - Polymorphism (specific behavior)
    """
    
    def get_category(self) -> str:
        """Override abstract method"""
        return "CPU"
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Polymorphic implementation"""
        if isinstance(other, Motherboard):
            # CPU-specific compatibility logic
            cpu_socket = self.get_attribute('socket', '')
            mb_socket = other.get_attribute('socket', '')
            return cpu_socket == mb_socket, "Socket check"
        return True, "No constraints"


# Usage demonstration
cpu = CPU('cpu_001', 'Intel i7-12700K', 329.99, {'socket': 'LGA1700'})
print(cpu.id)          # Property access
cpu.price = 299.99     # Property setter
print(cpu)             # __str__ method
```

## Common OOP Mistakes to Avoid

❌ **Don't access private attributes directly**
```python
# Wrong
print(cpu.__id)  # AttributeError

# Correct
print(cpu.id)    # Use property
```

❌ **Don't forget to call super().__init__()**
```python
class CPU(Component):
    def __init__(self, ...):
        super().__init__(...)  # Initialize parent class
        # Then add CPU-specific initialization
```

❌ **Don't instantiate abstract classes**
```python
# Wrong
comp = Component(...)  # TypeError

# Correct
cpu = CPU(...)  # Use concrete subclass
```

✅ **Do use type hints**
```python
def get_component(self, id: str) -> Optional[Component]:
    pass
```

✅ **Do validate in setters**
```python
@price.setter
def price(self, value: float) -> None:
    if value < 0:
        raise ValueError("Invalid price")
    self.__price = value
```

✅ **Do use composition over inheritance**
```python
# Good: Build HAS components
class Build:
    def __init__(self):
        self.components = []

# Avoid: Build IS A component (doesn't make sense)
```

## Testing OOP Code

```python
# Test encapsulation
cpu = CPU(...)
try:
    cpu.__id  # Should fail
    print("❌ Encapsulation broken")
except AttributeError:
    print("✓ Encapsulation working")

# Test polymorphism
components = [cpu, gpu, ram]
for comp in components:
    print(comp.get_category())  # Different for each

# Test singleton
db1 = DatabaseManager()
db2 = DatabaseManager()
print(f"Singleton: {db1 is db2}")  # Should be True

# Test factory
cpu = ComponentFactory.create_component('CPU', ...)
print(f"Type: {type(cpu).__name__}")  # Should be CPU
```

## Summary Checklist

✅ Abstract Base Classes (ABC)  
✅ Private Attributes (`__attribute`)  
✅ Property Decorators (`@property`)  
✅ Inheritance (Component → CPU)  
✅ Polymorphism (is_compatible_with)  
✅ Encapsulation (controlled access)  
✅ Composition (Build contains Components)  
✅ Singleton Pattern (DatabaseManager)  
✅ Factory Pattern (ComponentFactory)  
✅ Strategy Pattern (PasswordHashStrategy)  
✅ Type Hints (all methods)  
✅ Validation (in setters)  
✅ Documentation (docstrings)
