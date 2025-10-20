"""
CLI demo script to test the PC builder backend without GUI.
"""

from pcbuilder.db import init_db, list_parts, load_sample_parts
from pcbuilder.models import Part, Build
from pcbuilder.compat import run_full_check


def main():
    print("PC Part Picker - CLI Demo")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Load sample data if database is empty
    parts = list_parts()
    if not parts:
        print("\nDatabase empty. Loading sample parts...")
        load_sample_parts()
        parts = list_parts()
    
    print(f"\nFound {len(parts)} parts in database")
    
    # Display parts by category
    categories = {}
    for part in parts:
        if part.category not in categories:
            categories[part.category] = []
        categories[part.category].append(part)
    
    for category, cat_parts in sorted(categories.items()):
        print(f"\n{category}:")
        for part in cat_parts:
            print(f"  - {part.name} (£{part.price:.2f})")
    
    # Build a test PC
    print("\n" + "=" * 50)
    print("Building a test PC...")
    
    # Select first CPU and compatible motherboard
    cpu = next((p for p in parts if p.category == "CPU"), None)
    mobo = next((p for p in parts if p.category == "Motherboard" and 
                 p.attributes.get("socket") == cpu.attributes.get("socket")), None)
    ram = next((p for p in parts if p.category == "RAM" and
                p.attributes.get("memory_type") == mobo.attributes.get("memory_type")), None)
    gpu = next((p for p in parts if p.category == "GPU"), None)
    psu = next((p for p in parts if p.category == "PSU"), None)
    case = next((p for p in parts if p.category == "Case"), None)
    storage = next((p for p in parts if p.category == "Storage"), None)
    cooler = next((p for p in parts if p.category == "Cooler"), None)
    
    build = Build(
        name="Demo Build",
        parts={
            "CPU": cpu,
            "Motherboard": mobo,
            "RAM": ram,
            "GPU": gpu,
            "PSU": psu,
            "Case": case,
            "Storage": storage,
            "Cooler": cooler
        }
    )
    
    print(f"\nBuild: {build.name}")
    for category, part in build.parts.items():
        if part:
            print(f"  {category}: {part.name}")
    
    print(f"\nTotal Price: £{build.total_price():.2f}")
    
    # Check compatibility
    print("\n" + "=" * 50)
    print("Compatibility Check:")
    results = run_full_check(build)
    
    for rule_id, passed, message in results:
        status = "✓" if passed else "✗"
        print(f"  {status} {message}")
    
    all_passed = all(passed for _, passed, _ in results)
    if all_passed:
        print("\n✅ All compatibility checks passed!")
    else:
        print("\n⚠️  Some compatibility issues detected.")


if __name__ == "__main__":
    main()
