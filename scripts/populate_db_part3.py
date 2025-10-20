"""Add RAM and Storage to database"""
import json
from pathlib import Path

data_file = Path(__file__).parent.parent / "data" / "complete_parts.json"
with open(data_file, 'r') as f:
    components = json.load(f)

# ============================================================================
# RAM - 20 Components (DDR4 & DDR5, Various Speeds & Capacities)
# ============================================================================
ram = [
    {"id": "ram-gskill-64gb-ddr5-6400", "name": "G.Skill Trident Z5 RGB 64GB (2x32GB) DDR5 6400MHz", "category": "RAM", "price": 239.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 6400}},
    {"id": "ram-corsair-64gb-ddr5-6000", "name": "Corsair Dominator Platinum RGB 64GB (2x32GB) DDR5 6000MHz", "category": "RAM", "price": 259.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 6000}},
    {"id": "ram-gskill-32gb-ddr5-6000", "name": "G.Skill Trident Z5 RGB 32GB (2x16GB) DDR5 6000MHz", "category": "RAM", "price": 129.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 6000}},
    {"id": "ram-kingston-32gb-ddr5-5600", "name": "Kingston FURY Beast 32GB (2x16GB) DDR5 5600MHz", "category": "RAM", "price": 109.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 5600}},
    {"id": "ram-corsair-32gb-ddr5-5200", "name": "Corsair Vengeance 32GB (2x16GB) DDR5 5200MHz", "category": "RAM", "price": 99.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 5200}},
    {"id": "ram-crucial-32gb-ddr5-4800", "name": "Crucial 32GB (2x16GB) DDR5 4800MHz", "category": "RAM", "price": 89.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 4800}},
    {"id": "ram-gskill-16gb-ddr5-6000", "name": "G.Skill Trident Z5 16GB (2x8GB) DDR5 6000MHz", "category": "RAM", "price": 79.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 6000}},
    {"id": "ram-corsair-16gb-ddr5-5200", "name": "Corsair Vengeance 16GB (2x8GB) DDR5 5200MHz", "category": "RAM", "price": 64.99, "attributes": {"memory_type": "DDR5", "sticks": 2, "speed": 5200}},
    {"id": "ram-gskill-64gb-ddr4-3600", "name": "G.Skill Ripjaws V 64GB (2x32GB) DDR4 3600MHz", "category": "RAM", "price": 159.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3600}},
    {"id": "ram-corsair-32gb-ddr4-3600", "name": "Corsair Vengeance RGB Pro 32GB (2x16GB) DDR4 3600MHz", "category": "RAM", "price": 79.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3600}},
    {"id": "ram-gskill-32gb-ddr4-3200", "name": "G.Skill Ripjaws V 32GB (2x16GB) DDR4 3200MHz", "category": "RAM", "price": 69.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3200}},
    {"id": "ram-kingston-32gb-ddr4-3200", "name": "Kingston FURY Beast 32GB (2x16GB) DDR4 3200MHz", "category": "RAM", "price": 64.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3200}},
    {"id": "ram-corsair-16gb-ddr4-3600", "name": "Corsair Vengeance LPX 16GB (2x8GB) DDR4 3600MHz", "category": "RAM", "price": 39.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3600}},
    {"id": "ram-gskill-16gb-ddr4-3200", "name": "G.Skill Aegis 16GB (2x8GB) DDR4 3200MHz", "category": "RAM", "price": 34.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3200}},
    {"id": "ram-crucial-16gb-ddr4-3200", "name": "Crucial Ballistix 16GB (2x8GB) DDR4 3200MHz", "category": "RAM", "price": 32.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3200}},
    {"id": "ram-teamgroup-16gb-ddr4-3200", "name": "Team T-FORCE VULCAN Z 16GB (2x8GB) DDR4 3200MHz", "category": "RAM", "price": 29.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3200}},
    {"id": "ram-kingston-16gb-ddr4-2666", "name": "Kingston ValueRAM 16GB (2x8GB) DDR4 2666MHz", "category": "RAM", "price": 27.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 2666}},
    {"id": "ram-corsair-8gb-ddr4-3200", "name": "Corsair Vengeance LPX 8GB (2x4GB) DDR4 3200MHz", "category": "RAM", "price": 24.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 3200}},
    {"id": "ram-gskill-64gb-ddr4-4000", "name": "G.Skill Trident Z Neo 64GB (2x32GB) DDR4 4000MHz", "category": "RAM", "price": 199.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 4000}},
    {"id": "ram-corsair-32gb-ddr4-4000", "name": "Corsair Dominator Platinum RGB 32GB (2x16GB) DDR4 4000MHz", "category": "RAM", "price": 149.99, "attributes": {"memory_type": "DDR4", "sticks": 2, "speed": 4000}}
]

components.extend(ram)
print(f"Added {len(ram)} RAM kits")

# ============================================================================
# Storage - 20 Components (NVMe SSDs, SATA SSDs, HDDs)
# ============================================================================
storage = [
    {"id": "ssd-samsung-990pro-4tb", "name": "Samsung 990 Pro 4TB NVMe Gen4 SSD", "category": "Storage", "price": 349.99, "attributes": {"capacity": 4000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-wd-black-sn850x-4tb", "name": "WD Black SN850X 4TB NVMe Gen4 SSD", "category": "Storage", "price": 329.99, "attributes": {"capacity": 4000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-crucial-t500-2tb", "name": "Crucial T500 2TB NVMe Gen4 SSD", "category": "Storage", "price": 189.99, "attributes": {"capacity": 2000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-samsung-990pro-2tb", "name": "Samsung 990 Pro 2TB NVMe Gen4 SSD", "category": "Storage", "price": 199.99, "attributes": {"capacity": 2000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-wd-black-sn850x-2tb", "name": "WD Black SN850X 2TB NVMe Gen4 SSD", "category": "Storage", "price": 179.99, "attributes": {"capacity": 2000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-kingston-fury-2tb", "name": "Kingston FURY Renegade 2TB NVMe Gen4 SSD", "category": "Storage", "price": 169.99, "attributes": {"capacity": 2000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-samsung-980pro-1tb", "name": "Samsung 980 Pro 1TB NVMe Gen4 SSD", "category": "Storage", "price": 109.99, "attributes": {"capacity": 1000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-wd-black-sn770-1tb", "name": "WD Black SN770 1TB NVMe Gen4 SSD", "category": "Storage", "price": 89.99, "attributes": {"capacity": 1000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-crucial-p5-plus-1tb", "name": "Crucial P5 Plus 1TB NVMe Gen4 SSD", "category": "Storage", "price": 79.99, "attributes": {"capacity": 1000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-kingston-nv2-1tb", "name": "Kingston NV2 1TB NVMe Gen4 SSD", "category": "Storage", "price": 59.99, "attributes": {"capacity": 1000, "interface": "NVMe PCIe 4.0"}},
    {"id": "ssd-crucial-p3-500gb", "name": "Crucial P3 500GB NVMe Gen3 SSD", "category": "Storage", "price": 39.99, "attributes": {"capacity": 500, "interface": "NVMe PCIe 3.0"}},
    {"id": "ssd-wd-blue-500gb", "name": "WD Blue SN570 500GB NVMe Gen3 SSD", "category": "Storage", "price": 42.99, "attributes": {"capacity": 500, "interface": "NVMe PCIe 3.0"}},
    {"id": "ssd-samsung-870evo-2tb", "name": "Samsung 870 EVO 2TB SATA SSD", "category": "Storage", "price": 149.99, "attributes": {"capacity": 2000, "interface": "SATA"}},
    {"id": "ssd-crucial-mx500-2tb", "name": "Crucial MX500 2TB SATA SSD", "category": "Storage", "price": 129.99, "attributes": {"capacity": 2000, "interface": "SATA"}},
    {"id": "ssd-samsung-870evo-1tb", "name": "Samsung 870 EVO 1TB SATA SSD", "category": "Storage", "price": 84.99, "attributes": {"capacity": 1000, "interface": "SATA"}},
    {"id": "ssd-crucial-mx500-1tb", "name": "Crucial MX500 1TB SATA SSD", "category": "Storage", "price": 69.99, "attributes": {"capacity": 1000, "interface": "SATA"}},
    {"id": "ssd-wd-blue-500gb-sata", "name": "WD Blue 500GB SATA SSD", "category": "Storage", "price": 44.99, "attributes": {"capacity": 500, "interface": "SATA"}},
    {"id": "hdd-seagate-barracuda-4tb", "name": "Seagate BarraCuda 4TB 7200RPM HDD", "category": "Storage", "price": 89.99, "attributes": {"capacity": 4000, "interface": "SATA"}},
    {"id": "hdd-wd-blue-2tb", "name": "WD Blue 2TB 7200RPM HDD", "category": "Storage", "price": 54.99, "attributes": {"capacity": 2000, "interface": "SATA"}},
    {"id": "hdd-seagate-barracuda-1tb", "name": "Seagate BarraCuda 1TB 7200RPM HDD", "category": "Storage", "price": 39.99, "attributes": {"capacity": 1000, "interface": "SATA"}}
]

components.extend(storage)
print(f"Added {len(storage)} Storage devices")

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(components, f, indent=4, ensure_ascii=False)

print(f"Total components: {len(components)}")
