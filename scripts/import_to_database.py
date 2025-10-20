"""Import complete components into the database"""
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pcbuilder.db import load_sample_parts, list_parts

# Load the complete parts JSON into database
json_path = Path(__file__).parent.parent / "data" / "complete_parts.json"

print("=" * 60)
print("IMPORTING COMPLETE COMPONENT DATABASE")
print("=" * 60)

print(f"\n📂 Loading from: {json_path}")
print(f"   File exists: {json_path.exists()}")

if not json_path.exists():
    print("❌ ERROR: complete_parts.json not found!")
    sys.exit(1)

# Import into database
load_sample_parts(json_path)

print("\n✅ Import complete!")

# Verify
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

parts = list_parts()
print(f"\nTotal parts in database: {len(parts)}")

# Count by category
categories = {}
for part in parts:
    cat = part["category"]
    categories[cat] = categories.get(cat, 0) + 1

print("\n📊 Parts by category:")
for cat, count in sorted(categories.items()):
    print(f"   {cat:15} {count:3} parts")

# Show sample parts
print("\n📝 Sample parts:")
for cat in ["CPU", "GPU", "RAM"]:
    cat_parts = [p for p in parts if p["category"] == cat][:3]
    print(f"\n{cat}:")
    for p in cat_parts:
        print(f"   • {p['name']} - £{p['price']:.2f}")

print("\n" + "=" * 60)
print("✅ DATABASE READY FOR USE!")
print("=" * 60)
