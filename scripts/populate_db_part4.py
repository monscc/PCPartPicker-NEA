"""Add PSUs, Cases, and Coolers to database"""
import json
from pathlib import Path

data_file = Path(__file__).parent.parent / "data" / "complete_parts.json"
with open(data_file, 'r') as f:
    components = json.load(f)

# ============================================================================
# PSUs - 20 Components (Various Wattages & Efficiency Ratings)
# ============================================================================
psus = [
    {"id": "psu-corsair-rm1000e-1000w", "name": "Corsair RM1000e 1000W 80+ Gold Fully Modular", "category": "PSU", "price": 149.99, "attributes": {"wattage": 1000, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-seasonic-focus-1000w", "name": "Seasonic FOCUS GX-1000 1000W 80+ Gold Fully Modular", "category": "PSU", "price": 159.99, "attributes": {"wattage": 1000, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-evga-supernova-850w-plat", "name": "EVGA SuperNOVA 850 P5 850W 80+ Platinum Fully Modular", "category": "PSU", "price": 139.99, "attributes": {"wattage": 850, "efficiency": "80+ Platinum", "modular": "Fully Modular"}},
    {"id": "psu-corsair-rm850x-850w", "name": "Corsair RM850x 850W 80+ Gold Fully Modular", "category": "PSU", "price": 129.99, "attributes": {"wattage": 850, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-be-quiet-straight-850w", "name": "be quiet! Straight Power 11 850W 80+ Gold Fully Modular", "category": "PSU", "price": 134.99, "attributes": {"wattage": 850, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-seasonic-focus-850w", "name": "Seasonic FOCUS GX-850 850W 80+ Gold Fully Modular", "category": "PSU", "price": 119.99, "attributes": {"wattage": 850, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-corsair-rm750x-750w", "name": "Corsair RM750x 750W 80+ Gold Fully Modular", "category": "PSU", "price": 109.99, "attributes": {"wattage": 750, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-evga-supernova-750w", "name": "EVGA SuperNOVA 750 GT 750W 80+ Gold Fully Modular", "category": "PSU", "price": 99.99, "attributes": {"wattage": 750, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-msi-mpg-a750gf-750w", "name": "MSI MPG A750GF 750W 80+ Gold Fully Modular", "category": "PSU", "price": 94.99, "attributes": {"wattage": 750, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-thermaltake-toughpower-750w", "name": "Thermaltake Toughpower GF1 750W 80+ Gold Fully Modular", "category": "PSU", "price": 89.99, "attributes": {"wattage": 750, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-corsair-rm650-650w", "name": "Corsair RM650 650W 80+ Gold Fully Modular", "category": "PSU", "price": 84.99, "attributes": {"wattage": 650, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-seasonic-focus-650w", "name": "Seasonic FOCUS GM-650 650W 80+ Gold Semi-Modular", "category": "PSU", "price": 74.99, "attributes": {"wattage": 650, "efficiency": "80+ Gold", "modular": "Semi-Modular"}},
    {"id": "psu-evga-br-600w", "name": "EVGA 600 BR 600W 80+ Bronze Non-Modular", "category": "PSU", "price": 49.99, "attributes": {"wattage": 600, "efficiency": "80+ Bronze", "modular": "Non-Modular"}},
    {"id": "psu-corsair-cx650-650w", "name": "Corsair CX650M 650W 80+ Bronze Semi-Modular", "category": "PSU", "price": 64.99, "attributes": {"wattage": 650, "efficiency": "80+ Bronze", "modular": "Semi-Modular"}},
    {"id": "psu-thermaltake-smart-500w", "name": "Thermaltake Smart 500W 80+ Non-Modular", "category": "PSU", "price": 39.99, "attributes": {"wattage": 500, "efficiency": "80+", "modular": "Non-Modular"}},
    {"id": "psu-evga-500w", "name": "EVGA 500 W1 500W 80+ Non-Modular", "category": "PSU", "price": 34.99, "attributes": {"wattage": 500, "efficiency": "80+", "modular": "Non-Modular"}},
    {"id": "psu-coolermaster-mwe-550w", "name": "Cooler Master MWE 550 White V2 550W 80+ Non-Modular", "category": "PSU", "price": 44.99, "attributes": {"wattage": 550, "efficiency": "80+", "modular": "Non-Modular"}},
    {"id": "psu-corsair-rm850e-850w", "name": "Corsair RM850e 850W 80+ Gold Fully Modular", "category": "PSU", "price": 119.99, "attributes": {"wattage": 850, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-be-quiet-pure-700w", "name": "be quiet! Pure Power 11 FM 700W 80+ Gold Fully Modular", "category": "PSU", "price": 99.99, "attributes": {"wattage": 700, "efficiency": "80+ Gold", "modular": "Fully Modular"}},
    {"id": "psu-antec-hcg-850w", "name": "Antec High Current Gamer 850W 80+ Gold Fully Modular", "category": "PSU", "price": 114.99, "attributes": {"wattage": 850, "efficiency": "80+ Gold", "modular": "Fully Modular"}}
]

components.extend(psus)
print(f"Added {len(psus)} PSUs")

# ============================================================================
# Cases - 20 Components (ATX, Micro-ATX, Mini-ITX)
# ============================================================================
cases = [
    {"id": "case-lian-li-o11-dynamic", "name": "Lian Li O11 Dynamic EVO ATX Mid Tower (Tempered Glass)", "category": "Case", "price": 159.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 420}},
    {"id": "case-corsair-5000d-airflow", "name": "Corsair 5000D AIRFLOW ATX Mid Tower (Tempered Glass)", "category": "Case", "price": 149.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 420}},
    {"id": "case-fractal-torrent", "name": "Fractal Design Torrent ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 199.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 461}},
    {"id": "case-nzxt-h7-flow", "name": "NZXT H7 Flow RGB ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 129.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 400}},
    {"id": "case-phanteks-p500a", "name": "Phanteks Eclipse P500A D-RGB ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 139.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 435}},
    {"id": "case-be-quiet-pure-base-500dx", "name": "be quiet! Pure Base 500DX ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 99.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 369}},
    {"id": "case-corsair-4000d-airflow", "name": "Corsair 4000D AIRFLOW ATX Mid Tower (Tempered Glass)", "category": "Case", "price": 94.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 360}},
    {"id": "case-nzxt-h510-flow", "name": "NZXT H510 Flow ATX Mid Tower (Tempered Glass)", "category": "Case", "price": 89.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 381}},
    {"id": "case-fractal-meshify-c", "name": "Fractal Design Meshify 2 Compact ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 119.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 360}},
    {"id": "case-coolermaster-td500", "name": "Cooler Master MasterBox TD500 Mesh ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 99.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 410}},
    {"id": "case-lian-li-lancool-215", "name": "Lian Li LANCOOL 215 ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 79.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 384}},
    {"id": "case-phanteks-p360a", "name": "Phanteks Eclipse P360A ATX Mid Tower (Tempered Glass, Mesh)", "category": "Case", "price": 69.99, "attributes": {"form_factor": "ATX", "max_gpu_length": 400}},
    {"id": "case-corsair-crystal-280x", "name": "Corsair Crystal 280X RGB Micro-ATX (Tempered Glass)", "category": "Case", "price": 149.99, "attributes": {"form_factor": "Micro-ATX", "max_gpu_length": 300}},
    {"id": "case-coolermaster-nr400", "name": "Cooler Master MasterBox NR400 Micro-ATX (Mesh)", "category": "Case", "price": 64.99, "attributes": {"form_factor": "Micro-ATX", "max_gpu_length": 410}},
    {"id": "case-fractal-meshify-c-mini", "name": "Fractal Design Meshify C Mini Micro-ATX (Tempered Glass, Mesh)", "category": "Case", "price": 89.99, "attributes": {"form_factor": "Micro-ATX", "max_gpu_length": 315}},
    {"id": "case-thermaltake-v200-tg", "name": "Thermaltake V200 Tempered Glass Micro-ATX", "category": "Case", "price": 54.99, "attributes": {"form_factor": "Micro-ATX", "max_gpu_length": 350}},
    {"id": "case-nzxt-h210i", "name": "NZXT H210i Mini-ITX (Tempered Glass)", "category": "Case", "price": 99.99, "attributes": {"form_factor": "Mini-ITX", "max_gpu_length": 325}},
    {"id": "case-coolermaster-nr200p", "name": "Cooler Master NR200P Mini-ITX (Tempered Glass, Mesh)", "category": "Case", "price": 89.99, "attributes": {"form_factor": "Mini-ITX", "max_gpu_length": 330}},
    {"id": "case-lian-li-a4-h2o", "name": "Lian Li A4-H2O X4 Mini-ITX (Tempered Glass, Mesh)", "category": "Case", "price": 139.99, "attributes": {"form_factor": "Mini-ITX", "max_gpu_length": 328}},
    {"id": "case-fractal-ridge", "name": "Fractal Design Ridge Mini-ITX (Tempered Glass, Mesh)", "category": "Case", "price": 149.99, "attributes": {"form_factor": "Mini-ITX", "max_gpu_length": 337}}
]

components.extend(cases)
print(f"Added {len(cases)} Cases")

# ============================================================================
# Coolers - 20 Components (Air & AIO Liquid Coolers)
# ============================================================================
coolers = [
    {"id": "cooler-nzxt-kraken-z73", "name": "NZXT Kraken Z73 RGB 360mm AIO Liquid Cooler", "category": "Cooler", "price": 259.99, "attributes": {"type": "AIO", "size": "360mm"}},
    {"id": "cooler-corsair-h150i-elite", "name": "Corsair iCUE H150i ELITE LCD 360mm AIO Liquid Cooler", "category": "Cooler", "price": 279.99, "attributes": {"type": "AIO", "size": "360mm"}},
    {"id": "cooler-arctic-liquid-360", "name": "Arctic Liquid Freezer II 360mm AIO Liquid Cooler", "category": "Cooler", "price": 99.99, "attributes": {"type": "AIO", "size": "360mm"}},
    {"id": "cooler-lian-li-galahad-360", "name": "Lian Li Galahad II Trinity 360mm AIO Liquid Cooler", "category": "Cooler", "price": 139.99, "attributes": {"type": "AIO", "size": "360mm"}},
    {"id": "cooler-corsair-h100i-rgb", "name": "Corsair iCUE H100i RGB Elite 240mm AIO Liquid Cooler", "category": "Cooler", "price": 139.99, "attributes": {"type": "AIO", "size": "240mm"}},
    {"id": "cooler-nzxt-kraken-240", "name": "NZXT Kraken 240 RGB 240mm AIO Liquid Cooler", "category": "Cooler", "price": 119.99, "attributes": {"type": "AIO", "size": "240mm"}},
    {"id": "cooler-arctic-liquid-240", "name": "Arctic Liquid Freezer II 240mm AIO Liquid Cooler", "category": "Cooler", "price": 69.99, "attributes": {"type": "AIO", "size": "240mm"}},
    {"id": "cooler-deepcool-le500", "name": "DeepCool LE500 240mm AIO Liquid Cooler", "category": "Cooler", "price": 59.99, "attributes": {"type": "AIO", "size": "240mm"}},
    {"id": "cooler-noctua-nhd15", "name": "Noctua NH-D15 Chromax Black Dual Tower Air Cooler", "category": "Cooler", "price": 109.99, "attributes": {"type": "Air", "size": "140mm"}},
    {"id": "cooler-be-quiet-dark-rock-pro4", "name": "be quiet! Dark Rock Pro 4 Air Cooler", "category": "Cooler", "price": 89.99, "attributes": {"type": "Air", "size": "135mm"}},
    {"id": "cooler-deepcool-ak620", "name": "DeepCool AK620 Dual Tower Air Cooler", "category": "Cooler", "price": 64.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-arctic-freezer-34", "name": "Arctic Freezer 34 eSports DUO Air Cooler", "category": "Cooler", "price": 44.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-coolermaster-hyper-212", "name": "Cooler Master Hyper 212 RGB Black Edition Air Cooler", "category": "Cooler", "price": 44.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-noctua-nhu12s", "name": "Noctua NH-U12S Redux Air Cooler", "category": "Cooler", "price": 49.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-be-quiet-pure-rock-2", "name": "be quiet! Pure Rock 2 Air Cooler", "category": "Cooler", "price": 39.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-id-cooling-se-224-xt", "name": "ID-COOLING SE-224-XT RGB Air Cooler", "category": "Cooler", "price": 29.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-deepcool-gammaxx-400", "name": "DeepCool GAMMAXX 400 V2 Air Cooler", "category": "Cooler", "price": 24.99, "attributes": {"type": "Air", "size": "120mm"}},
    {"id": "cooler-arctic-freezer-7x", "name": "Arctic Freezer 7 X Compact Air Cooler", "category": "Cooler", "price": 19.99, "attributes": {"type": "Air", "size": "92mm"}},
    {"id": "cooler-corsair-h60", "name": "Corsair iCUE H60 RGB Elite 120mm AIO Liquid Cooler", "category": "Cooler", "price": 79.99, "attributes": {"type": "AIO", "size": "120mm"}},
    {"id": "cooler-thermaltake-th120", "name": "Thermaltake TH120 ARGB Sync 120mm AIO Liquid Cooler", "category": "Cooler", "price": 64.99, "attributes": {"type": "AIO", "size": "120mm"}}
]

components.extend(coolers)
print(f"Added {len(coolers)} Coolers")

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(components, f, indent=4, ensure_ascii=False)

print(f"\n✅ COMPLETE! Total components: {len(components)}")
print(f"📊 Breakdown:")
print(f"   - CPUs: 20")
print(f"   - GPUs: 20")
print(f"   - Motherboards: 20")
print(f"   - RAM: 20")
print(f"   - Storage: 20")
print(f"   - PSUs: 20")
print(f"   - Cases: 20")
print(f"   - Coolers: 20")
