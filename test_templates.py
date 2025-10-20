"""Test template builds with actual database"""
from pcbuilder.templates import get_template_summary, load_template_build

print("=" * 60)
print("TEMPLATE BUILDS VERIFICATION")
print("=" * 60)

for template_id in ['budget', 'mid_range', 'high_end']:
    summary = get_template_summary(template_id)
    parts = load_template_build(template_id)
    
    print(f"\n{summary['name']}")
    print(f"Target Price: {summary['target_price']}")
    print(f"Actual Price: £{summary['actual_price']:.2f}")
    print(f"Components Found: {summary['component_count']}/8")
    
    if summary['missing_components'] > 0:
        print(f"⚠️  Missing: {summary['missing_components']} components")
        missing = [cat for cat, part in parts.items() if part is None]
        print(f"   Categories: {', '.join(missing)}")
    else:
        print("✅ All components found!")
    
    print("\nComponent List:")
    for category in ["CPU", "Motherboard", "RAM", "GPU", "PSU", "Case", "Storage", "Cooler"]:
        part = parts.get(category)
        if part:
            print(f"  ✓ {category}: {part['name']} (£{part['price']:.2f})")
        else:
            print(f"  ✗ {category}: NOT FOUND")
    
    print("-" * 60)

print("\n✅ Template verification complete!")
