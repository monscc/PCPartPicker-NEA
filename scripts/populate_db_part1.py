"""
Comprehensive PC Components Database Population Script
Adds 20 top components for each category with realistic UK prices and specs
"""
import json
from pathlib import Path

# Define comprehensive component list
components = []

# ============================================================================
# CPUs - 20 Components (Mix of Intel and AMD, Budget to High-End)
# ============================================================================
cpus = [
    {"id": "cpu-9800x3d", "name": "AMD Ryzen 7 9800X3D", "category": "CPU", "price": 479.99, "attributes": {"socket": "AM5", "cores": 8, "threads": 16, "boost_clock": 5.2, "power_draw": 120}},
    {"id": "cpu-9950x3d", "name": "AMD Ryzen 9 9950X3D", "category": "CPU", "price": 699.99, "attributes": {"socket": "AM5", "cores": 16, "threads": 32, "boost_clock": 5.7, "power_draw": 170}},
    {"id": "cpu-i9-14900k", "name": "Intel Core i9-14900K", "category": "CPU", "price": 435.99, "attributes": {"socket": "LGA1700", "cores": 24, "threads": 32, "boost_clock": 6.0, "power_draw": 253}},
    {"id": "cpu-i7-14700k", "name": "Intel Core i7-14700K", "category": "CPU", "price": 339.99, "attributes": {"socket": "LGA1700", "cores": 20, "threads": 28, "boost_clock": 5.6, "power_draw": 253}},
    {"id": "cpu-9700x", "name": "AMD Ryzen 7 9700X", "category": "CPU", "price": 318.99, "attributes": {"socket": "AM5", "cores": 8, "threads": 16, "boost_clock": 5.5, "power_draw": 65}},
    {"id": "cpu-9600x", "name": "AMD Ryzen 5 9600X", "category": "CPU", "price": 239.99, "attributes": {"socket": "AM5", "cores": 6, "threads": 12, "boost_clock": 5.4, "power_draw": 65}},
    {"id": "cpu-i5-14600k", "name": "Intel Core i5-14600K", "category": "CPU", "price": 234.99, "attributes": {"socket": "LGA1700", "cores": 14, "threads": 20, "boost_clock": 5.3, "power_draw": 181}},
    {"id": "cpu-5700x3d", "name": "AMD Ryzen 7 5700X3D", "category": "CPU", "price": 229.99, "attributes": {"socket": "AM4", "cores": 8, "threads": 16, "boost_clock": 4.1, "power_draw": 105}},
    {"id": "cpu-8600g", "name": "AMD Ryzen 5 8600G", "category": "CPU", "price": 169.99, "attributes": {"socket": "AM5", "cores": 6, "threads": 12, "boost_clock": 5.0, "power_draw": 65}},
    {"id": "cpu-i5-12400f", "name": "Intel Core i5-12400F", "category": "CPU", "price": 109.99, "attributes": {"socket": "LGA1700", "cores": 6, "threads": 12, "boost_clock": 4.4, "power_draw": 117}},
    {"id": "cpu-5600", "name": "AMD Ryzen 5 5600", "category": "CPU", "price": 106.99, "attributes": {"socket": "AM4", "cores": 6, "threads": 12, "boost_clock": 4.6, "power_draw": 65}},
    {"id": "cpu-7800x3d", "name": "AMD Ryzen 7 7800X3D", "category": "CPU", "price": 369.99, "attributes": {"socket": "AM5", "cores": 8, "threads": 16, "boost_clock": 5.0, "power_draw": 120}},
    {"id": "cpu-i9-13900k", "name": "Intel Core i9-13900K", "category": "CPU", "price": 449.99, "attributes": {"socket": "LGA1700", "cores": 24, "threads": 32, "boost_clock": 5.8, "power_draw": 253}},
    {"id": "cpu-i5-13400f", "name": "Intel Core i5-13400F", "category": "CPU", "price": 159.99, "attributes": {"socket": "LGA1700", "cores": 10, "threads": 16, "boost_clock": 4.6, "power_draw": 148}},
    {"id": "cpu-7900x", "name": "AMD Ryzen 9 7900X", "category": "CPU", "price": 379.99, "attributes": {"socket": "AM5", "cores": 12, "threads": 24, "boost_clock": 5.4, "power_draw": 170}},
    {"id": "cpu-5600x3d", "name": "AMD Ryzen 5 5600X3D", "category": "CPU", "price": 199.99, "attributes": {"socket": "AM4", "cores": 6, "threads": 12, "boost_clock": 4.4, "power_draw": 105}},
    {"id": "cpu-i7-13700k", "name": "Intel Core i7-13700K", "category": "CPU", "price": 329.99, "attributes": {"socket": "LGA1700", "cores": 16, "threads": 24, "boost_clock": 5.4, "power_draw": 253}},
    {"id": "cpu-7600x", "name": "AMD Ryzen 5 7600X", "category": "CPU", "price": 209.99, "attributes": {"socket": "AM5", "cores": 6, "threads": 12, "boost_clock": 5.3, "power_draw": 105}},
    {"id": "cpu-i3-12100f", "name": "Intel Core i3-12100F", "category": "CPU", "price": 79.99, "attributes": {"socket": "LGA1700", "cores": 4, "threads": 8, "boost_clock": 4.3, "power_draw": 89}},
    {"id": "cpu-5500", "name": "AMD Ryzen 5 5500", "category": "CPU", "price": 89.99, "attributes": {"socket": "AM4", "cores": 6, "threads": 12, "boost_clock": 4.2, "power_draw": 65}}
]

components.extend(cpus)

print(f"Added {len(cpus)} CPUs")

# Save to file
output_file = Path(__file__).parent.parent / "data" / "complete_parts.json"
output_file.parent.mkdir(exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(components, f, indent=4, ensure_ascii=False)

print(f"Saved to {output_file}")
print(f"Total components so far: {len(components)}")
