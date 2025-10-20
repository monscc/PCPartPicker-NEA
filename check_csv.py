"""Check CSV column mapping"""
import csv

with open('data/uk_components_complete.csv', 'r') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    
    print(f"Header has {len(header)} columns:")
    for i, col in enumerate(header, 1):
        print(f"{i}. {col}")
    
    print("\n" + "="*60)
    print("PSU Row Analysis:")
    print("="*60)
    
    for row in reader:
        if row['category'] == 'PSU':
            print(f"\nPSU: {row['name']}")
            print("\nNon-empty fields:")
            for key, value in row.items():
                if value:
                    print(f"  {key}: {value}")
            break
