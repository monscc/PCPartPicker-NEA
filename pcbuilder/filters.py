"""
Component filtering system with unique filters for each category
Includes binary search optimization for price-based filtering
"""
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from .search_algorithms import binary_search_by_price, binary_search_range, linear_search_by_price
from .models import Component, ComponentFactory


@dataclass
class Filter:
    """Represents a single filter criterion"""
    name: str
    display_name: str
    filter_func: Callable[[Dict], bool]
    category: str


class ComponentFilters:
    """Manages filters for different component categories"""
    
    def __init__(self):
        self.filters = self._initialize_filters()
    
    def _initialize_filters(self) -> Dict[str, List[Filter]]:
        """Initialize all filters for each component category"""
        return {
            "CPU": self._get_cpu_filters(),
            "Motherboard": self._get_motherboard_filters(),
            "RAM": self._get_ram_filters(),
            "GPU": self._get_gpu_filters(),
            "PSU": self._get_psu_filters(),
            "Case": self._get_case_filters(),
            "Storage": self._get_storage_filters(),
            "Cooler": self._get_cooler_filters()
        }
    
    def _get_cpu_filters(self) -> List[Filter]:
        """CPU-specific filters"""
        return [
            Filter("6_cores", "6+ Cores", 
                   lambda p: p.get("attributes", {}).get("cores", 0) >= 6, "CPU"),
            Filter("8_cores", "8+ Cores", 
                   lambda p: p.get("attributes", {}).get("cores", 0) >= 8, "CPU"),
            Filter("12_cores", "12+ Cores", 
                   lambda p: p.get("attributes", {}).get("cores", 0) >= 12, "CPU"),
            Filter("unlocked", "Unlocked (K/X)", 
                   lambda p: any(x in p.get("name", "").upper() for x in ["K", "X", "KF", "KS"]), "CPU"),
            Filter("integrated_gpu", "Integrated Graphics", 
                   lambda p: "F" not in p.get("name", "") or "G" in p.get("name", ""), "CPU"),
        ]
    
    def _get_motherboard_filters(self) -> List[Filter]:
        """Motherboard-specific filters"""
        return [
            Filter("atx", "ATX Size", 
                   lambda p: p.get("attributes", {}).get("form_factor", "").upper() == "ATX", "Motherboard"),
            Filter("micro_atx", "Micro-ATX Size", 
                   lambda p: p.get("attributes", {}).get("form_factor", "").upper() == "MICRO-ATX", "Motherboard"),
            Filter("mini_itx", "Mini-ITX Size", 
                   lambda p: p.get("attributes", {}).get("form_factor", "").upper() == "MINI-ITX", "Motherboard"),
            Filter("wifi", "Built-in WiFi", 
                   lambda p: "wifi" in p.get("name", "").lower() or 
                            p.get("attributes", {}).get("wifi", False), "Motherboard"),
            Filter("ddr5", "DDR5 Support", 
                   lambda p: "DDR5" in p.get("attributes", {}).get("ram_type", ""), "Motherboard"),
            Filter("ddr4", "DDR4 Support", 
                   lambda p: "DDR4" in p.get("attributes", {}).get("ram_type", ""), "Motherboard"),
        ]
    
    def _get_ram_filters(self) -> List[Filter]:
        """RAM-specific filters"""
        return [
            Filter("16gb", "16GB+", 
                   lambda p: self._parse_ram_capacity(p) >= 16, "RAM"),
            Filter("32gb", "32GB+", 
                   lambda p: self._parse_ram_capacity(p) >= 32, "RAM"),
            Filter("ddr4", "DDR4", 
                   lambda p: "DDR4" in p.get("name", ""), "RAM"),
            Filter("ddr5", "DDR5", 
                   lambda p: "DDR5" in p.get("name", ""), "RAM"),
            Filter("3200mhz", "3200 MHz+", 
                   lambda p: p.get("attributes", {}).get("speed", 0) >= 3200, "RAM"),
            Filter("3600mhz", "3600 MHz+", 
                   lambda p: p.get("attributes", {}).get("speed", 0) >= 3600, "RAM"),
            Filter("rgb", "RGB Lighting", 
                   lambda p: "rgb" in p.get("name", "").lower(), "RAM"),
        ]
    
    def _get_gpu_filters(self) -> List[Filter]:
        """GPU-specific filters"""
        return [
            Filter("8gb_vram", "8GB+ VRAM", 
                   lambda p: p.get("attributes", {}).get("vram", 0) >= 8, "GPU"),
            Filter("12gb_vram", "12GB+ VRAM", 
                   lambda p: p.get("attributes", {}).get("vram", 0) >= 12, "GPU"),
            Filter("16gb_vram", "16GB+ VRAM", 
                   lambda p: p.get("attributes", {}).get("vram", 0) >= 16, "GPU"),
            Filter("nvidia", "NVIDIA", 
                   lambda p: "nvidia" in p.get("name", "").lower() or "rtx" in p.get("name", "").lower() or "gtx" in p.get("name", "").lower(), "GPU"),
            Filter("amd", "AMD", 
                   lambda p: "amd" in p.get("name", "").lower() or "radeon" in p.get("name", "").lower() or "rx" in p.get("name", "").lower(), "GPU"),
            Filter("ray_tracing", "Ray Tracing", 
                   lambda p: "rtx" in p.get("name", "").lower() or "rx 7" in p.get("name", "").lower(), "GPU"),
        ]
    
    def _get_psu_filters(self) -> List[Filter]:
        """PSU-specific filters"""
        return [
            Filter("modular", "Fully Modular", 
                   lambda p: "fully modular" in p.get("attributes", {}).get("modular", "").lower(), "PSU"),
            Filter("semi_modular", "Semi-Modular", 
                   lambda p: "semi" in p.get("attributes", {}).get("modular", "").lower(), "PSU"),
            Filter("non_modular", "Non-Modular", 
                   lambda p: "non" in p.get("attributes", {}).get("modular", "").lower(), "PSU"),
            Filter("650w", "650W+", 
                   lambda p: p.get("attributes", {}).get("wattage", 0) >= 650, "PSU"),
            Filter("750w", "750W+", 
                   lambda p: p.get("attributes", {}).get("wattage", 0) >= 750, "PSU"),
            Filter("850w", "850W+", 
                   lambda p: p.get("attributes", {}).get("wattage", 0) >= 850, "PSU"),
            Filter("80plus_gold", "80+ Gold", 
                   lambda p: "gold" in p.get("attributes", {}).get("efficiency", "").lower(), "PSU"),
            Filter("80plus_platinum", "80+ Platinum", 
                   lambda p: "platinum" in p.get("attributes", {}).get("efficiency", "").lower(), "PSU"),
        ]
    
    def _get_case_filters(self) -> List[Filter]:
        """Case-specific filters"""
        return [
            Filter("atx", "ATX Support", 
                   lambda p: "ATX" in p.get("attributes", {}).get("form_factor", ""), "Case"),
            Filter("micro_atx", "Micro-ATX Support", 
                   lambda p: "Micro-ATX" in p.get("attributes", {}).get("form_factor", "") or "ATX" in p.get("attributes", {}).get("form_factor", ""), "Case"),
            Filter("mini_itx", "Mini-ITX Support", 
                   lambda p: "Mini-ITX" in p.get("attributes", {}).get("form_factor", ""), "Case"),
            Filter("tempered_glass", "Tempered Glass", 
                   lambda p: "glass" in p.get("name", "").lower() or "tg" in p.get("name", "").lower(), "Case"),
            Filter("rgb", "RGB Lighting", 
                   lambda p: "rgb" in p.get("name", "").lower(), "Case"),
            Filter("mesh", "Mesh Front Panel", 
                   lambda p: "mesh" in p.get("name", "").lower(), "Case"),
        ]
    
    def _get_storage_filters(self) -> List[Filter]:
        """Storage-specific filters"""
        return [
            Filter("ssd", "SSD", 
                   lambda p: "SSD" in p.get("name", ""), "Storage"),
            Filter("hdd", "HDD", 
                   lambda p: "HDD" in p.get("name", ""), "Storage"),
            Filter("nvme", "NVMe", 
                   lambda p: "NVMe" in p.get("attributes", {}).get("interface", ""), "Storage"),
            Filter("sata", "SATA", 
                   lambda p: "SATA" in p.get("attributes", {}).get("interface", ""), "Storage"),
            Filter("500gb", "500GB+", 
                   lambda p: self._parse_storage_capacity(p) >= 500, "Storage"),
            Filter("1tb", "1TB+", 
                   lambda p: self._parse_storage_capacity(p) >= 1000, "Storage"),
            Filter("2tb", "2TB+", 
                   lambda p: self._parse_storage_capacity(p) >= 2000, "Storage"),
            Filter("pcie4", "PCIe 4.0", 
                   lambda p: "4.0" in p.get("attributes", {}).get("interface", "") or "Gen4" in p.get("name", ""), "Storage"),
        ]
    
    def _get_cooler_filters(self) -> List[Filter]:
        """CPU Cooler-specific filters"""
        return [
            Filter("air", "Air Cooler", 
                   lambda p: "air" in p.get("attributes", {}).get("type", "").lower() or "tower" in p.get("name", "").lower(), "Cooler"),
            Filter("aio", "AIO Liquid", 
                   lambda p: "aio" in p.get("attributes", {}).get("type", "").lower() or "liquid" in p.get("name", "").lower(), "Cooler"),
            Filter("120mm", "120mm", 
                   lambda p: "120mm" in p.get("name", ""), "Cooler"),
            Filter("240mm", "240mm+", 
                   lambda p: any(x in p.get("name", "") for x in ["240mm", "280mm", "360mm", "420mm"]), "Cooler"),
            Filter("rgb", "RGB Lighting", 
                   lambda p: "rgb" in p.get("name", "").lower(), "Cooler"),
            Filter("quiet", "Low Noise", 
                   lambda p: "silent" in p.get("name", "").lower() or "quiet" in p.get("name", "").lower(), "Cooler"),
        ]
    
    def _parse_ram_capacity(self, part: Dict) -> int:
        """Extract RAM capacity from name (e.g., '32GB (2x16GB)' -> 32)"""
        import re
        name = part.get("name", "")
        match = re.search(r'(\d+)GB', name)
        return int(match.group(1)) if match else 0
    
    def _parse_storage_capacity(self, part: Dict) -> int:
        """Extract storage capacity in GB (handles both string '1TB' and int 500)"""
        import re
        capacity = part.get("attributes", {}).get("capacity", 0)
        
        # If it's already an integer, return it
        if isinstance(capacity, int):
            return capacity
        
        # If it's a string, parse it
        if isinstance(capacity, str):
            # Check for TB
            if "TB" in capacity.upper():
                match = re.search(r'(\d+)TB', capacity.upper())
                if match:
                    return int(match.group(1)) * 1000  # Convert TB to GB
            # Check for GB
            elif "GB" in capacity.upper():
                match = re.search(r'(\d+)GB', capacity.upper())
                if match:
                    return int(match.group(1))
        
        return 0
    
    def get_filters_for_category(self, category: str) -> List[Filter]:
        """Get all available filters for a category"""
        return self.filters.get(category, [])
    
    def apply_filters(self, parts: List[Dict], category: str, active_filters: List[str]) -> List[Dict]:
        """Apply active filters to a list of parts"""
        if not active_filters:
            return parts
        
        category_filters = self.get_filters_for_category(category)
        filter_map = {f.name: f for f in category_filters}
        
        filtered_parts = []
        for part in parts:
            # Part must pass ALL active filters
            if all(filter_map[fname].filter_func(part) for fname in active_filters if fname in filter_map):
                filtered_parts.append(part)
        
        return filtered_parts


def find_component_by_price(parts: List[Dict], target_price: float, use_binary_search: bool = True) -> Optional[Dict]:
    """
    Find component closest to target price using binary or linear search
    
    Time Complexity:
    - Binary search: O(log n) if already sorted, O(n log n) if needs sorting
    - Linear search: O(n) but no sorting needed
    
    Args:
        parts: List of component dictionaries
        target_price: Target price to match
        use_binary_search: If True, use binary search (faster for large lists)
        
    Returns:
        Component dict closest to target price, or None
    """
    if not parts:
        return None
    
    # Convert dicts to Component objects for algorithm
    components = []
    for part in parts:
        try:
            component = ComponentFactory.create_component(
                part['id'], part['name'], part['category'],
                part['price'], part.get('attributes', {})
            )
            components.append(component)
        except Exception:
            continue
    
    if not components:
        return None
    
    if use_binary_search:
        # Sort by price for binary search
        sorted_components = sorted(components, key=lambda c: c.price)
        result = binary_search_by_price(sorted_components, target_price)
    else:
        # Linear search on unsorted list
        result = linear_search_by_price(components, target_price)
    
    if result:
        return result.to_dict()
    return None


def find_components_in_price_range(
    parts: List[Dict],
    min_price: float,
    max_price: float,
    use_binary_search: bool = True
) -> List[Dict]:
    """
    Find all components within a price range
    
    Time Complexity:
    - Binary search: O(log n + k) where k is number of results
    - Linear search: O(n)
    
    Args:
        parts: List of component dictionaries
        min_price: Minimum price (inclusive)
        max_price: Maximum price (inclusive)
        use_binary_search: If True, use binary search approach
        
    Returns:
        List of component dicts within price range
    """
    if not parts or min_price > max_price:
        return []
    
    if use_binary_search:
        # Convert to Component objects
        components = []
        for part in parts:
            try:
                component = ComponentFactory.create_component(
                    part['id'], part['name'], part['category'],
                    part['price'], part.get('attributes', {})
                )
                components.append(component)
            except Exception:
                continue
        
        # Sort and use binary search range
        sorted_components = sorted(components, key=lambda c: c.price)
        result_components = binary_search_range(sorted_components, min_price, max_price)
        return [c.to_dict() for c in result_components]
    else:
        # Linear filtering (traditional approach)
        return [p for p in parts if min_price <= p['price'] <= max_price]


# Global instance
component_filters = ComponentFilters()
