"""Manual test for compatibility checker"""
from pcbuilder.db import list_parts
from pcbuilder.compat import run_full_check

# Get some parts
all_parts = list_parts()

# Build a test configuration
parts_dict = {
    "CPU": None,
    "Motherboard": None,
    "RAM": None,
    "GPU": None,
    "PSU": None,
    "Case": None,
    "Storage": None,
    "Cooler": None
}

# Select specific parts
for part in all_parts:
    if part["category"] == "CPU" and "i5-12400F" in part["name"]:
        parts_dict["CPU"] = part
        print(f"Selected CPU: {part['name']}")
        print(f"  Attributes: {part['attributes']}")
    elif part["category"] == "Motherboard" and "B660M" in part["name"]:
        parts_dict["Motherboard"] = part
        print(f"Selected Motherboard: {part['name']}")
        print(f"  Attributes: {part['attributes']}")
    elif part["category"] == "PSU" and "650W" in part["name"]:
        parts_dict["PSU"] = part
        print(f"Selected PSU: {part['name']}")
        print(f"  Attributes: {part['attributes']}")
    elif part["category"] == "GPU" and "RTX 4060" in part["name"]:
        parts_dict["GPU"] = part
        print(f"Selected GPU: {part['name']}")
        print(f"  Attributes: {part['attributes']}")

print("\n" + "="*60)
print("Running compatibility check...")
print("="*60)

results = run_full_check(parts_dict)

for rule_id, passed, message in results:
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {message}")
