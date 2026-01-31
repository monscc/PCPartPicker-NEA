# Template PC Builds System
# Provides pre-configured builds for Budget, Mid-Range, and High-End tiers
from typing import Dict, Optional, List
from .database_manager import get_database_manager


class TemplateBuild:
    # Represents a template PC build
    def __init__(self, name: str, description: str, target_price: str, components: Dict[str, str]):
        self.name = name
        self.description = description
        self.target_price = target_price
        self.components = components  # Category -> Part name mapping
    
    def to_dict(self) -> dict:
        # Convert to dictionary format
        return {
            'name': self.name,
            'description': self.description,
            'target_price': self.target_price,
            'components': self.components
        }


# Define the three template builds
TEMPLATE_BUILDS = {
    'budget': TemplateBuild(
        name="💰 Budget Gaming Build",
        description="Perfect entry-level gaming PC for 1080p gaming and everyday tasks. "
                   "Great for esports titles and casual gaming on a tight budget.",
        target_price="£500-700",
        components={
            'CPU': 'Intel Core i3-12100F',
            'Motherboard': 'MSI B660M PRO-A DDR4',
            'RAM': 'Corsair Vengeance LPX 16GB (2x8GB) DDR4 3200MHz',
            'GPU': 'AMD Radeon RX 6600 8GB',
            'PSU': 'Corsair CV550 550W 80+ Bronze',
            'Case': 'NZXT H510 Compact ATX Mid-Tower',
            'Storage': 'Samsung 870 EVO 500GB 2.5" SATA SSD',
            'Cooler': 'Cooler Master Hyper 212 Black Edition'
        }
    ),
    'mid_range': TemplateBuild(
        name="🎮 Mid-Range Performance Build",
        description="Excellent all-round gaming PC for 1440p gaming and content creation. "
                   "Balances performance and value with room for upgrades.",
        target_price="£800-1200",
        components={
            'CPU': 'Intel Core i5-12400F',
            'Motherboard': 'MSI MAG B760M MORTAR WIFI DDR4',
            'RAM': 'G.Skill Trident Z5 RGB 32GB (2x16GB) DDR5 6000MHz',
            'GPU': 'NVIDIA GeForce RTX 4060 Ti 8GB',
            'PSU': 'Corsair RM650e 650W 80+ Gold',
            'Case': 'Corsair 4000D Airflow ATX Mid-Tower',
            'Storage': 'Samsung 980 PRO 1TB M.2 NVMe Gen4 SSD',
            'Cooler': 'be quiet! Dark Rock 4'
        }
    ),
    'high_end': TemplateBuild(
        name="🚀 High-End Enthusiast Build",
        description="Top-tier gaming and workstation PC for 4K gaming, streaming, and heavy workloads. "
                   "No compromises on performance.",
        target_price="£1500+",
        components={
            'CPU': 'AMD Ryzen 7 7800X3D',
            'Motherboard': 'ASUS ROG CROSSHAIR X670E HERO',
            'RAM': 'G.Skill Trident Z5 RGB 32GB (2x16GB) DDR5 6000MHz',
            'GPU': 'NVIDIA GeForce RTX 4070 Ti 12GB',
            'PSU': 'Corsair RM850x 850W 80+ Gold',
            'Case': 'Lian Li O11 Dynamic EVO',
            'Storage': 'Samsung 990 PRO 2TB M.2 NVMe Gen4 SSD',
            'Cooler': 'Noctua NH-D15 chromax.black'
        }
    )
}


def get_template_builds() -> Dict[str, TemplateBuild]:
    # Get all template builds
    return TEMPLATE_BUILDS


def get_template_build(template_id: str) -> Optional[TemplateBuild]:
    # Get a specific template build by ID
    return TEMPLATE_BUILDS.get(template_id)


def load_template_build(template_id: str) -> Optional[Dict[str, Optional[dict]]]:
    # Load a template build and resolve component names to actual part objects
    #
    # Returns:
    # Dictionary mapping category to part object (or None if not found)
    template = get_template_build(template_id)
    if not template:
        return None
    
    # Get all parts from database
    db = get_database_manager()
    components = db.get_all_components()
    all_parts = [comp.to_dict() for comp in components]
    parts_by_name = {part['name']: part for part in all_parts}
    
    # Build the selected_parts dictionary
    selected_parts = {
        'CPU': None,
        'Motherboard': None,
        'RAM': None,
        'GPU': None,
        'PSU': None,
        'Case': None,
        'Storage': None,
        'Cooler': None
    }
    
    # Resolve template component names to actual parts
    for category, part_name in template.components.items():
        if part_name in parts_by_name:
            selected_parts[category] = parts_by_name[part_name]
        else:
            # Try partial match if exact match not found
            for name, part in parts_by_name.items():
                if part_name.lower() in name.lower() and part['category'] == category:
                    selected_parts[category] = part
                    break
    
    return selected_parts


def calculate_template_price(template_id: str) -> float:
    # Calculate the total price of a template build
    parts = load_template_build(template_id)
    if not parts:
        return 0.0
    
    total = 0.0
    for part in parts.values():
        if part:
            total += part.get('price', 0.0)
    
    return total


def get_template_summary(template_id: str) -> Optional[dict]:
    # Get a summary of a template build including price and component count
    #
    # Returns:
    # Dictionary with name, description, target_price, actual_price, and component_count
    template = get_template_build(template_id)
    if not template:
        return None
    
    parts = load_template_build(template_id)
    actual_price = calculate_template_price(template_id)
    component_count = sum(1 for p in parts.values() if p is not None) if parts else 0
    
    return {
        'id': template_id,
        'name': template.name,
        'description': template.description,
        'target_price': template.target_price,
        'actual_price': actual_price,
        'component_count': component_count,
        'missing_components': 8 - component_count
    }
