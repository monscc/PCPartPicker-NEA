"""
Manual data collection helper for PC Part Picker.

This tool creates CSV templates for manually entering component data
from UK retailers (Overclockers, Scan, Amazon UK, etc.)
"""

import csv
import os


def create_manual_entry_template(filename='data/manual_entry.csv'):
    """
    Create a CSV template for manual data entry.
    
    Opens the file in your default CSV editor after creation.
    """
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # All possible columns
    headers = [
        'id', 'name', 'category', 'price', 'source', 'url',
        'socket', 'power_draw', 'cores', 'threads',
        'form_factor', 'memory_type', 'memory_slots', 'sticks', 'speed',
        'gpu_length', 'memory',
        'wattage', 'efficiency',
        'capacity', 'interface',
        'mobo_support', 'case_max_gpu_length',
        'supported_sockets', 'type'
    ]
    
    # Example rows with helpful data
    examples = [
        # CPU example
        {
            'id': 'cpu-i5-12400f',
            'name': 'Intel Core i5-12400F',
            'category': 'CPU',
            'price': '159.99',
            'source': 'Overclockers UK',
            'url': 'https://www.overclockers.co.uk/...',
            'socket': 'LGA1700',
            'power_draw': '117',
            'cores': '6',
            'threads': '12'
        },
        # Motherboard example
        {
            'id': 'mobo-b660m-pro',
            'name': 'MSI B660M PRO-A DDR4',
            'category': 'Motherboard',
            'price': '104.99',
            'source': 'Scan UK',
            'url': 'https://www.scan.co.uk/...',
            'socket': 'LGA1700',
            'form_factor': 'micro-ATX',
            'memory_type': 'DDR4',
            'memory_slots': '4'
        },
        # RAM example
        {
            'id': 'ram-vengeance-16gb',
            'name': 'Corsair Vengeance LPX 16GB (2x8GB) DDR4 3200MHz',
            'category': 'RAM',
            'price': '34.99',
            'source': 'Amazon UK',
            'url': 'https://www.amazon.co.uk/...',
            'memory_type': 'DDR4',
            'sticks': '2',
            'speed': '3200'
        },
        # GPU example
        {
            'id': 'gpu-rtx4060',
            'name': 'NVIDIA GeForce RTX 4060 8GB',
            'category': 'GPU',
            'price': '289.99',
            'source': 'Overclockers UK',
            'url': 'https://www.overclockers.co.uk/...',
            'power_draw': '115',
            'gpu_length': '244',
            'memory': '8GB'
        },
        # PSU example
        {
            'id': 'psu-rm750e',
            'name': 'Corsair RM750e 650W 80+ Gold',
            'category': 'PSU',
            'price': '69.99',
            'source': 'Scan UK',
            'url': 'https://www.scan.co.uk/...',
            'wattage': '650',
            'efficiency': '80+ Gold'
        },
        # Case example
        {
            'id': 'case-h510',
            'name': 'NZXT H510 Mid Tower',
            'category': 'Case',
            'price': '74.99',
            'source': 'Amazon UK',
            'url': 'https://www.amazon.co.uk/...',
            'mobo_support': 'ATX,micro-ATX,mini-ITX',
            'case_max_gpu_length': '381'
        },
        # Storage example
        {
            'id': 'storage-970evo-1tb',
            'name': 'Samsung 970 EVO Plus 1TB NVMe SSD',
            'category': 'Storage',
            'price': '54.99',
            'source': 'Overclockers UK',
            'url': 'https://www.overclockers.co.uk/...',
            'power_draw': '5',
            'capacity': '1TB',
            'interface': 'NVMe'
        },
        # Cooler example
        {
            'id': 'cooler-hyper212',
            'name': 'Cooler Master Hyper 212 Black Edition',
            'category': 'Cooler',
            'price': '29.99',
            'source': 'Scan UK',
            'url': 'https://www.scan.co.uk/...',
            'power_draw': '2',
            'supported_sockets': 'LGA1700,AM4',
            'type': 'Air'
        }
    ]
    
    # Write CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(examples)
    
    print(f"✅ Created template: {filename}")
    print(f"   ({len(examples)} example rows included)")
    return filename


def validate_csv(filename):
    """
    Validate that CSV has required fields and correct format.
    """
    required_cols = ['id', 'name', 'category', 'price']
    
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            # Check required columns exist
            missing = [col for col in required_cols if col not in headers]
            if missing:
                print(f"❌ Missing required columns: {', '.join(missing)}")
                return False
            
            # Validate each row
            issues = []
            row_count = 0
            
            for i, row in enumerate(reader, start=2):
                row_count += 1
                
                # Check required fields not empty
                for col in required_cols:
                    if not row.get(col, '').strip():
                        issues.append(f"Row {i}: Missing {col}")
                
                # Check price is numeric
                try:
                    price = row.get('price', '').strip()
                    if price:
                        float(price)
                except ValueError:
                    issues.append(f"Row {i}: Invalid price '{price}'")
            
            if issues:
                print(f"❌ Found {len(issues)} issue(s):")
                for issue in issues[:10]:  # Show first 10
                    print(f"   - {issue}")
                if len(issues) > 10:
                    print(f"   ... and {len(issues) - 10} more")
                return False
            
            print(f"✅ CSV valid: {row_count} rows, all checks passed")
            return True
    
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False


def show_instructions():
    """Display helpful instructions for manual data collection."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              Manual PC Component Data Collection                     ║
╚══════════════════════════════════════════════════════════════════════╝

📝 STEP-BY-STEP GUIDE:

1. OPEN THE CSV TEMPLATE
   - Location: data/manual_entry.csv
   - Open in: Excel, Google Sheets, or any spreadsheet app
   - 8 example rows are already filled in

2. VISIT UK RETAILERS
   Recommended sites:
   • Overclockers UK  → overclockers.co.uk
   • Scan Computers   → scan.co.uk
   • Amazon UK        → amazon.co.uk
   • CCL Online       → cclonline.com

3. FOR EACH COMPONENT:
   a) Navigate to product page
   b) Copy product name (exactly as shown)
   c) Copy price (remove £ symbol - just the number)
   d) Note specifications (see column guide below)
   e) Add new row to CSV

4. COLUMN GUIDE:

   Required for ALL components:
   • id       → Unique identifier (e.g., cpu-i5-12400f)
   • name     → Full product name
   • category → CPU, Motherboard, RAM, GPU, PSU, Case, Storage, Cooler
   • price    → Numeric price WITHOUT £ (e.g., 159.99)

   Optional (fill if available):
   • source   → Retailer name
   • url      → Product page URL

   Category-specific attributes:
   
   CPU:
   • socket      → LGA1700, AM4, AM5
   • power_draw  → Wattage (e.g., 117)
   • cores       → Number of cores (e.g., 6)
   • threads     → Number of threads (e.g., 12)

   Motherboard:
   • socket        → LGA1700, AM4, AM5
   • form_factor   → ATX, micro-ATX, mini-ITX
   • memory_type   → DDR4, DDR5
   • memory_slots  → Number of RAM slots (e.g., 4)

   RAM:
   • memory_type → DDR4, DDR5
   • sticks      → Number of sticks (e.g., 2 for dual-channel)
   • speed       → MHz (e.g., 3200, 6000)

   GPU:
   • power_draw → Wattage (e.g., 115)
   • gpu_length → Length in mm (e.g., 244)
   • memory     → VRAM (e.g., 8GB, 12GB)

   PSU:
   • wattage    → Power output (e.g., 650, 750)
   • efficiency → 80+ Bronze, 80+ Gold, etc.

   Case:
   • mobo_support        → Supported sizes (e.g., ATX,micro-ATX,mini-ITX)
   • case_max_gpu_length → Max GPU length in mm (e.g., 381)

   Storage:
   • capacity   → Size (e.g., 1TB, 2TB)
   • interface  → NVMe, SATA
   • power_draw → Wattage (usually 4-7W)

   Cooler:
   • supported_sockets → Compatible sockets (e.g., LGA1700,AM4)
   • type              → Air, AIO
   • power_draw        → Wattage (usually 2-6W)

5. SAVE YOUR WORK OFTEN!
   - Save CSV after adding each 5-10 components
   - Backup file periodically

6. VALIDATE BEFORE IMPORTING:
   python manual_collector.py --validate data/manual_entry.csv

7. IMPORT TO DATABASE:
   python manage_db.py import data/manual_entry.csv

═══════════════════════════════════════════════════════════════════════

📊 RECOMMENDED QUANTITIES:

   • CPUs:         8-10 components  (mix Intel/AMD, various sockets)
   • Motherboards: 8-10 components  (various sockets and form factors)
   • RAM:          6-8 components   (DDR4 and DDR5, different capacities)
   • GPUs:         8-10 components  (budget to high-end)
   • PSUs:         5-6 components   (different wattages)
   • Cases:        3-4 components   (different sizes)
   • Storage:      4-5 components   (NVMe and SATA)
   • Coolers:      3-4 components   (air and AIO)
   
   TOTAL: 50-60 components = 2-3 hours work

═══════════════════════════════════════════════════════════════════════

💡 TIPS:

   • Start with popular components (best sellers)
   • Mix budget and high-end options
   • Include both Intel and AMD for CPUs
   • Include both DDR4 and DDR5 for RAM/Motherboards
   • Note: Remove £ symbol from prices (just numbers)
   • IDs should be lowercase with hyphens (cpu-i5-12400f)
   • Leave attributes blank if not applicable

═══════════════════════════════════════════════════════════════════════
""")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--validate':
            if len(sys.argv) < 3:
                print("Usage: python manual_collector.py --validate <filename>")
                sys.exit(1)
            validate_csv(sys.argv[2])
        elif sys.argv[1] == '--help':
            show_instructions()
        else:
            print("Unknown option. Use --help or --validate")
    else:
        # Default: create template and show instructions
        print("\n🎯 PC Part Picker - Manual Data Collection Tool\n")
        
        filename = create_manual_entry_template()
        
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print(f"1. Open the file: {filename}")
        print("2. Delete the example rows (keep the header!)")
        print("3. Visit UK retailers and add your components")
        print("4. Save frequently!")
        print("\n💡 For detailed instructions, run:")
        print("   python manual_collector.py --help")
        print("\n📋 To validate your CSV before importing:")
        print(f"   python manual_collector.py --validate {filename}")
        print("\n📥 When ready, import to database:")
        print(f"   python manage_db.py import {filename}")
        print("="*70)
        
        # Try to open the file
        print("\n🚀 Attempting to open CSV in default editor...")
        try:
            import subprocess
            import platform
            
            if platform.system() == 'Windows':
                os.startfile(filename)
                print("✅ Opened in default CSV editor!")
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', filename])
                print("✅ Opened in default CSV editor!")
            else:  # Linux
                subprocess.run(['xdg-open', filename])
                print("✅ Opened in default CSV editor!")
        except Exception as e:
            print(f"⚠️  Could not auto-open (open manually): {e}")


if __name__ == '__main__':
    main()
