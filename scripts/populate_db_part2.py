"""Add GPUs and Motherboards to database"""
import json
from pathlib import Path

# Load existing components
data_file = Path(__file__).parent.parent / "data" / "complete_parts.json"
with open(data_file, 'r') as f:
    components = json.load(f)

# ============================================================================
# GPUs - 20 Components (NVIDIA & AMD, Budget to High-End)
# ============================================================================
gpus = [
    {"id": "gpu-rtx4090", "name": "NVIDIA GeForce RTX 4090 24GB", "category": "GPU", "price": 1599.99, "attributes": {"power_draw": 450, "gpu_length": 304, "vram": 24}},
    {"id": "gpu-rtx4080-super", "name": "NVIDIA GeForce RTX 4080 SUPER 16GB", "category": "GPU", "price": 999.99, "attributes": {"power_draw": 320, "gpu_length": 304, "vram": 16}},
    {"id": "gpu-rtx4070ti-super", "name": "NVIDIA GeForce RTX 4070 Ti SUPER 16GB", "category": "GPU", "price": 799.99, "attributes": {"power_draw": 285, "gpu_length": 267, "vram": 16}},
    {"id": "gpu-rtx4070-super", "name": "NVIDIA GeForce RTX 4070 SUPER 12GB", "category": "GPU", "price": 599.99, "attributes": {"power_draw": 220, "gpu_length": 267, "vram": 12}},
    {"id": "gpu-rtx4070", "name": "NVIDIA GeForce RTX 4070 12GB", "category": "GPU", "price": 549.99, "attributes": {"power_draw": 200, "gpu_length": 244, "vram": 12}},
    {"id": "gpu-rtx4060ti", "name": "NVIDIA GeForce RTX 4060 Ti 8GB", "category": "GPU", "price": 399.99, "attributes": {"power_draw": 160, "gpu_length": 244, "vram": 8}},
    {"id": "gpu-rtx4060", "name": "NVIDIA GeForce RTX 4060 8GB", "category": "GPU", "price": 289.99, "attributes": {"power_draw": 115, "gpu_length": 224, "vram": 8}},
    {"id": "gpu-rtx3060", "name": "NVIDIA GeForce RTX 3060 12GB", "category": "GPU", "price": 269.99, "attributes": {"power_draw": 170, "gpu_length": 242, "vram": 12}},
    {"id": "gpu-rx7900xtx", "name": "AMD Radeon RX 7900 XTX 24GB", "category": "GPU", "price": 949.99, "attributes": {"power_draw": 355, "gpu_length": 287, "vram": 24}},
    {"id": "gpu-rx7900xt", "name": "AMD Radeon RX 7900 XT 20GB", "category": "GPU", "price": 749.99, "attributes": {"power_draw": 300, "gpu_length": 287, "vram": 20}},
    {"id": "gpu-rx7800xt", "name": "AMD Radeon RX 7800 XT 16GB", "category": "GPU", "price": 499.99, "attributes": {"power_draw": 263, "gpu_length": 270, "vram": 16}},
    {"id": "gpu-rx7700xt", "name": "AMD Radeon RX 7700 XT 12GB", "category": "GPU", "price": 419.99, "attributes": {"power_draw": 245, "gpu_length": 270, "vram": 12}},
    {"id": "gpu-rx7600xt", "name": "AMD Radeon RX 7600 XT 16GB", "category": "GPU", "price": 329.99, "attributes": {"power_draw": 190, "gpu_length": 245, "vram": 16}},
    {"id": "gpu-rx7600", "name": "AMD Radeon RX 7600 8GB", "category": "GPU", "price": 249.99, "attributes": {"power_draw": 165, "gpu_length": 245, "vram": 8}},
    {"id": "gpu-rx6700xt", "name": "AMD Radeon RX 6700 XT 12GB", "category": "GPU", "price": 329.99, "attributes": {"power_draw": 230, "gpu_length": 267, "vram": 12}},
    {"id": "gpu-rx6650xt", "name": "AMD Radeon RX 6650 XT 8GB", "category": "GPU", "price": 259.99, "attributes": {"power_draw": 180, "gpu_length": 242, "vram": 8}},
    {"id": "gpu-rx6600", "name": "AMD Radeon RX 6600 8GB", "category": "GPU", "price": 199.99, "attributes": {"power_draw": 132, "gpu_length": 190, "vram": 8}},
    {"id": "gpu-rtx3070", "name": "NVIDIA GeForce RTX 3070 8GB", "category": "GPU", "price": 449.99, "attributes": {"power_draw": 220, "gpu_length": 267, "vram": 8}},
    {"id": "gpu-rtx3050", "name": "NVIDIA GeForce RTX 3050 8GB", "category": "GPU", "price": 229.99, "attributes": {"power_draw": 130, "gpu_length": 232, "vram": 8}},
    {"id": "gpu-gtx1660super", "name": "NVIDIA GeForce GTX 1660 SUPER 6GB", "category": "GPU", "price": 189.99, "attributes": {"power_draw": 125, "gpu_length": 229, "vram": 6}}
]

components.extend(gpus)
print(f"Added {len(gpus)} GPUs")

# ============================================================================
# Motherboards - 20 Components (Intel & AMD, Various Form Factors)
# ============================================================================
motherboards = [
    {"id": "mobo-x670e-hero", "name": "ASUS ROG Crosshair X670E Hero", "category": "Motherboard", "price": 629.99, "attributes": {"socket": "AM5", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-z790-apex", "name": "ASUS ROG Maximus Z790 Apex", "category": "Motherboard", "price": 649.99, "attributes": {"socket": "LGA1700", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 2, "wifi": True}},
    {"id": "mobo-x670e-tomahawk", "name": "MSI MAG X670E Tomahawk WiFi", "category": "Motherboard", "price": 319.99, "attributes": {"socket": "AM5", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-z790-gaming", "name": "ASUS TUF Gaming Z790-Plus WiFi", "category": "Motherboard", "price": 289.99, "attributes": {"socket": "LGA1700", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-b650-strix", "name": "ASUS ROG STRIX B650E-F Gaming WiFi", "category": "Motherboard", "price": 269.99, "attributes": {"socket": "AM5", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-b760-tomahawk", "name": "MSI MAG B760 Tomahawk WiFi", "category": "Motherboard", "price": 219.99, "attributes": {"socket": "LGA1700", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-b650-aorus", "name": "Gigabyte B650 AORUS Elite AX", "category": "Motherboard", "price": 199.99, "attributes": {"socket": "AM5", "form_factor": "ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-b660-pro", "name": "MSI PRO B660M-A DDR4", "category": "Motherboard", "price": 109.99, "attributes": {"socket": "LGA1700", "form_factor": "Micro-ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": False}},
    {"id": "mobo-b550-strix", "name": "ASUS ROG STRIX B550-F Gaming", "category": "Motherboard", "price": 159.99, "attributes": {"socket": "AM4", "form_factor": "ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": False}},
    {"id": "mobo-b550-tomahawk", "name": "MSI MAG B550 Tomahawk", "category": "Motherboard", "price": 149.99, "attributes": {"socket": "AM4", "form_factor": "ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": False}},
    {"id": "mobo-b450-max", "name": "MSI B450 Tomahawk MAX II", "category": "Motherboard", "price": 89.99, "attributes": {"socket": "AM4", "form_factor": "ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": False}},
    {"id": "mobo-z690-gaming", "name": "Gigabyte Z690 Gaming X DDR4", "category": "Motherboard", "price": 179.99, "attributes": {"socket": "LGA1700", "form_factor": "ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": False}},
    {"id": "mobo-b650m-mortar", "name": "MSI MAG B650M Mortar WiFi", "category": "Motherboard", "price": 189.99, "attributes": {"socket": "AM5", "form_factor": "Micro-ATX", "ram_type": "DDR5", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-b760m-plus", "name": "ASUS PRIME B760M-A WiFi D4", "category": "Motherboard", "price": 139.99, "attributes": {"socket": "LGA1700", "form_factor": "Micro-ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-x570-tuf", "name": "ASUS TUF Gaming X570-Plus WiFi", "category": "Motherboard", "price": 189.99, "attributes": {"socket": "AM4", "form_factor": "ATX", "ram_type": "DDR4", "memory_slots": 4, "wifi": True}},
    {"id": "mobo-h610m-hdv", "name": "ASRock H610M-HDV/M.2", "category": "Motherboard", "price": 69.99, "attributes": {"socket": "LGA1700", "form_factor": "Micro-ATX", "ram_type": "DDR4", "memory_slots": 2, "wifi": False}},
    {"id": "mobo-a520m-hdv", "name": "ASRock A520M-HDV", "category": "Motherboard", "price": 59.99, "attributes": {"socket": "AM4", "form_factor": "Micro-ATX", "ram_type": "DDR4", "memory_slots": 2, "wifi": False}},
    {"id": "mobo-b650-itx", "name": "ASUS ROG STRIX B650E-I Gaming WiFi", "category": "Motherboard", "price": 299.99, "attributes": {"socket": "AM5", "form_factor": "Mini-ITX", "ram_type": "DDR5", "memory_slots": 2, "wifi": True}},
    {"id": "mobo-z790-itx", "name": "Gigabyte Z790 I AORUS ULTRA", "category": "Motherboard", "price": 349.99, "attributes": {"socket": "LGA1700", "form_factor": "Mini-ITX", "ram_type": "DDR5", "memory_slots": 2, "wifi": True}},
    {"id": "mobo-b550-itx", "name": "ASUS ROG STRIX B550-I Gaming", "category": "Motherboard", "price": 209.99, "attributes": {"socket": "AM4", "form_factor": "Mini-ITX", "ram_type": "DDR4", "memory_slots": 2, "wifi": True}}
]

components.extend(motherboards)
print(f"Added {len(motherboards)} Motherboards")

# Save
with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(components, f, indent=4, ensure_ascii=False)

print(f"Total components: {len(components)}")
