"""
Core Data Models with Object-Oriented Design
Implements abstract base classes, encapsulation, and polymorphism
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class ComponentCategory(Enum):
    """Enumeration of all component categories"""
    CPU = "CPU"
    MOTHERBOARD = "Motherboard"
    RAM = "RAM"
    GPU = "GPU"
    STORAGE = "Storage"
    PSU = "PSU"
    CASE = "Case"
    COOLER = "Cooler"


class Component(ABC):
    """
    Abstract base class for all PC components
    Demonstrates: Abstraction, Encapsulation with private attributes
    """
    
    def __init__(self, component_id: str, name: str, price: float, attributes: Dict[str, Any]):
        # Private attributes using name mangling
        self.__id: str = component_id
        self.__name: str = name
        self.__price: float = price
        self.__attributes: Dict[str, Any] = attributes
    
    # Property decorators for controlled access (Encapsulation)
    @property
    def id(self) -> str:
        """Get component ID (read-only)"""
        return self.__id
    
    @property
    def name(self) -> str:
        """Get component name (read-only)"""
        return self.__name
    
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
    
    @property
    def attributes(self) -> Dict[str, Any]:
        """Get component attributes (returns copy for encapsulation)"""
        return self.__attributes.copy()
    
    def get_attribute(self, key: str, default: Any = None) -> Any:
        """Safely get a specific attribute"""
        return self.__attributes.get(key, default)
    
    @abstractmethod
    def get_category(self) -> ComponentCategory:
        """Abstract method: Each component must define its category"""
        pass
    
    @abstractmethod
    def is_compatible_with(self, other: 'Component') -> tuple[bool, str]:
        """Abstract method: Check compatibility with another component"""
        pass
    
    @abstractmethod
    def get_specifications(self) -> Dict[str, Any]:
        """Abstract method: Get formatted specifications for display"""
        pass
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}: {self.__name} (£{self.__price:.2f})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return f"{self.__class__.__name__}(id='{self.__id}', name='{self.__name}')"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary for serialization"""
        return {
            'id': self.__id,
            'name': self.__name,
            'category': self.get_category().value,
            'price': self.__price,
            'attributes': self.__attributes
        }


class CPU(Component):
    """Concrete implementation of CPU component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.CPU
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check CPU compatibility with other components"""
        if isinstance(other, Motherboard):
            cpu_socket = self.get_attribute('socket', '')
            mb_socket = other.get_attribute('socket', '')
            if cpu_socket == mb_socket:
                return True, "Compatible sockets"
            return False, f"Incompatible sockets: CPU {cpu_socket} vs Motherboard {mb_socket}"
        return True, "No compatibility constraints"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get CPU specifications"""
        return {
            'Cores': self.get_attribute('cores', 'N/A'),
            'Base Clock': f"{self.get_attribute('base_clock', 'N/A')} GHz",
            'Boost Clock': f"{self.get_attribute('boost_clock', 'N/A')} GHz",
            'Socket': self.get_attribute('socket', 'N/A'),
            'TDP': f"{self.get_attribute('tdp', 'N/A')} W"
        }


class Motherboard(Component):
    """Concrete implementation of Motherboard component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.MOTHERBOARD
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check motherboard compatibility"""
        if isinstance(other, CPU):
            return other.is_compatible_with(self)
        elif isinstance(other, RAM):
            mb_ram_type = self.get_attribute('ram_type', '')
            # RAM type is in the name typically
            if 'DDR5' in other.name and 'DDR5' in mb_ram_type:
                return True, "Compatible RAM type (DDR5)"
            elif 'DDR4' in other.name and 'DDR4' in mb_ram_type:
                return True, "Compatible RAM type (DDR4)"
            return False, "Incompatible RAM types"
        return True, "No compatibility constraints"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get motherboard specifications"""
        return {
            'Socket': self.get_attribute('socket', 'N/A'),
            'Form Factor': self.get_attribute('form_factor', 'N/A'),
            'RAM Type': self.get_attribute('ram_type', 'N/A'),
            'Max RAM': self.get_attribute('max_ram', 'N/A'),
            'WiFi': 'Yes' if self.get_attribute('wifi', False) else 'No'
        }


class GPU(Component):
    """Concrete implementation of GPU component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.GPU
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check GPU compatibility"""
        if isinstance(other, PSU):
            gpu_tdp = self.get_attribute('tdp', 0)
            # Basic check - PSU should have enough headroom
            return True, f"GPU TDP: {gpu_tdp}W"
        return True, "No compatibility constraints"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get GPU specifications"""
        return {
            'VRAM': f"{self.get_attribute('vram', 'N/A')} GB",
            'Interface': self.get_attribute('interface', 'N/A'),
            'TDP': f"{self.get_attribute('tdp', 'N/A')} W",
            'Length': f"{self.get_attribute('length', 'N/A')} mm"
        }


class RAM(Component):
    """Concrete implementation of RAM component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.RAM
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check RAM compatibility"""
        if isinstance(other, Motherboard):
            return other.is_compatible_with(self)
        return True, "No compatibility constraints"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get RAM specifications"""
        return {
            'Capacity': self.get_attribute('capacity', 'N/A'),
            'Speed': f"{self.get_attribute('speed', 'N/A')} MHz",
            'Type': self.get_attribute('type', 'N/A'),
            'Latency': self.get_attribute('latency', 'N/A')
        }


class Storage(Component):
    """Concrete implementation of Storage component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.STORAGE
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check storage compatibility"""
        return True, "Storage is universally compatible"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get storage specifications"""
        return {
            'Capacity': self.get_attribute('capacity', 'N/A'),
            'Type': self.get_attribute('type', 'N/A'),
            'Interface': self.get_attribute('interface', 'N/A'),
            'Read Speed': self.get_attribute('read_speed', 'N/A')
        }


class PSU(Component):
    """Concrete implementation of PSU component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.PSU
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check PSU compatibility"""
        return True, "PSU compatibility checked at build level"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get PSU specifications"""
        return {
            'Wattage': f"{self.get_attribute('wattage', 'N/A')} W",
            'Efficiency': self.get_attribute('efficiency', 'N/A'),
            'Modular': self.get_attribute('modular', 'N/A')
        }


class Case(Component):
    """Concrete implementation of Case component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.CASE
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check case compatibility"""
        if isinstance(other, Motherboard):
            case_ff = self.get_attribute('form_factor', '')
            mb_ff = other.get_attribute('form_factor', '')
            # Cases typically support multiple form factors
            if mb_ff in case_ff or mb_ff == case_ff:
                return True, "Compatible form factors"
            return False, f"Incompatible: Case supports {case_ff}, Motherboard is {mb_ff}"
        return True, "No compatibility constraints"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get case specifications"""
        return {
            'Form Factor': self.get_attribute('form_factor', 'N/A'),
            'Max GPU Length': f"{self.get_attribute('max_gpu_length', 'N/A')} mm",
            'Fans Included': self.get_attribute('fans', 'N/A')
        }


class Cooler(Component):
    """Concrete implementation of Cooler component"""
    
    def get_category(self) -> ComponentCategory:
        return ComponentCategory.COOLER
    
    def is_compatible_with(self, other: Component) -> tuple[bool, str]:
        """Check cooler compatibility"""
        return True, "Cooler compatibility depends on socket and case clearance"
    
    def get_specifications(self) -> Dict[str, Any]:
        """Get cooler specifications"""
        return {
            'Type': self.get_attribute('type', 'N/A'),
            'Fan Size': self.get_attribute('fan_size', 'N/A'),
            'Height': f"{self.get_attribute('height', 'N/A')} mm",
            'TDP Rating': f"{self.get_attribute('tdp_rating', 'N/A')} W"
        }


class ComponentFactory:
    """
    Factory pattern for creating component instances
    Demonstrates: Factory design pattern, Polymorphism
    """
    
    _component_map = {
        'CPU': CPU,
        'Motherboard': Motherboard,
        'GPU': GPU,
        'RAM': RAM,
        'Storage': Storage,
        'PSU': PSU,
        'Case': Case,
        'Cooler': Cooler
    }
    
    @classmethod
    def create_component(cls, component_id: str, name: str, category: str, 
                        price: float, attributes: Dict[str, Any]) -> Component:
        """Create appropriate component instance based on category"""
        component_class = cls._component_map.get(category)
        if component_class is None:
            raise ValueError(f"Unknown component category: {category}")
        return component_class(component_id, name, price, attributes)


class Build:
    """
    Represents a PC build with encapsulated components
    Demonstrates: Encapsulation, Composition
    """
    
    def __init__(self, build_id: Optional[int], name: str, user_id: int):
        # Private attributes
        self.__build_id: Optional[int] = build_id
        self.__name: str = name
        self.__user_id: int = user_id
        self.__components: Dict[str, Optional[Component]] = {
            'CPU': None,
            'Motherboard': None,
            'RAM': None,
            'GPU': None,
            'Storage': None,
            'PSU': None,
            'Case': None,
            'Cooler': None
        }
        self.__created_at: datetime = datetime.now()
        self.__share_key: Optional[str] = None
    
    @property
    def build_id(self) -> Optional[int]:
        """Get build ID"""
        return self.__build_id
    
    @build_id.setter
    def build_id(self, value: int) -> None:
        """Set build ID (for database assignment)"""
        self.__build_id = value
    
    @property
    def name(self) -> str:
        """Get build name"""
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        """Set build name with validation"""
        if not value or len(value) < 3:
            raise ValueError("Build name must be at least 3 characters")
        self.__name = value
    
    @property
    def user_id(self) -> int:
        """Get user ID"""
        return self.__user_id
    
    @property
    def share_key(self) -> Optional[str]:
        """Get share key"""
        return self.__share_key
    
    @share_key.setter
    def share_key(self, value: str) -> None:
        """Set share key"""
        self.__share_key = value
    
    def add_component(self, component: Component) -> None:
        """Add a component to the build"""
        category = component.get_category().value
        self.__components[category] = component
    
    def remove_component(self, category: str) -> None:
        """Remove a component from the build"""
        if category in self.__components:
            self.__components[category] = None
    
    def get_component(self, category: str) -> Optional[Component]:
        """Get a component by category"""
        return self.__components.get(category)
    
    def get_all_components(self) -> Dict[str, Optional[Component]]:
        """Get all components (returns copy for encapsulation)"""
        return self.__components.copy()
    
    def calculate_total_price(self) -> float:
        """Calculate total price of all components"""
        return sum(comp.price for comp in self.__components.values() if comp is not None)
    
    def calculate_total_wattage(self) -> int:
        """Calculate total power consumption"""
        total = 0
        for comp in self.__components.values():
            if comp is not None:
                tdp = comp.get_attribute('tdp', 0)
                if isinstance(tdp, (int, float)):
                    total += int(tdp)
        return total
    
    def is_complete(self) -> bool:
        """Check if build has all essential components"""
        essential = ['CPU', 'Motherboard', 'RAM', 'Storage', 'PSU', 'Case']
        return all(self.__components.get(cat) is not None for cat in essential)
    
    def get_compatibility_issues(self) -> List[str]:
        """Check for compatibility issues between components"""
        issues = []
        components = [c for c in self.__components.values() if c is not None]
        
        # Check pairwise compatibility
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                compatible, message = comp1.is_compatible_with(comp2)
                if not compatible:
                    issues.append(f"{comp1.get_category().value} <-> {comp2.get_category().value}: {message}")
        
        # Check PSU wattage
        if self.__components['PSU'] is not None:
            psu_wattage = self.__components['PSU'].get_attribute('wattage', 0)
            total_wattage = self.calculate_total_wattage()
            if isinstance(psu_wattage, (int, float)) and psu_wattage < total_wattage * 1.2:
                issues.append(f"PSU may be underpowered: {psu_wattage}W PSU for {total_wattage}W system")
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert build to dictionary for serialization"""
        return {
            'id': self.__build_id,
            'name': self.__name,
            'user_id': self.__user_id,
            'components': {
                cat: comp.to_dict() if comp else None 
                for cat, comp in self.__components.items()
            },
            'total_price': self.calculate_total_price(),
            'created_at': self.__created_at.isoformat(),
            'share_key': self.__share_key
        }
    
    def __str__(self) -> str:
        """String representation"""
        comp_count = sum(1 for c in self.__components.values() if c is not None)
        return f"Build: {self.__name} ({comp_count}/8 components, £{self.calculate_total_price():.2f})"
