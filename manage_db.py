#!/usr/bin/env python3
"""
Database management CLI tool for PC Part Picker.

Commands:
    stats       - Show database statistics
    import      - Import parts from CSV file
    export      - Export parts to CSV file
    template    - Create a CSV template file
    clear       - Clear all parts from database

Usage:
    python manage_db.py stats
    python manage_db.py import data/my_parts.csv
    python manage_db.py export data/backup.csv
    python manage_db.py template data/template.csv
    python manage_db.py clear
"""

import sys
from pcbuilder.importer import (
    import_parts_from_csv,
    export_parts_to_csv,
    clear_parts_database,
    get_part_statistics,
    create_csv_template
)


def print_usage():
    """Print usage information."""
    print(__doc__)


def cmd_stats():
    """Show database statistics."""
    stats = get_part_statistics()
    
    print(f"\n📊 Database Statistics")
    print(f"{'='*50}")
    print(f"Total parts: {stats['total_parts']}")
    
    if stats['total_parts'] > 0:
        print(f"\nParts by category:")
        for category, count in sorted(stats['by_category'].items()):
            print(f"  {category}: {count}")
        
        print(f"\nPrice range: £{stats['price_min']:.2f} - £{stats['price_max']:.2f}")
        print(f"Average price: £{stats['price_avg']:.2f}")
    else:
        print("\n⚠️  Database is empty. Import some parts to get started!")


def cmd_import(filepath):
    """Import parts from CSV file."""
    print(f"\n📥 Importing parts from: {filepath}")
    
    try:
        count = import_parts_from_csv(filepath)
        print(f"✅ Successfully imported {count} parts!")
        print(f"\nRun 'python manage_db.py stats' to see updated statistics.")
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during import: {e}")
        sys.exit(1)


def cmd_export(filepath, category=None):
    """Export parts to CSV file."""
    print(f"\n📤 Exporting parts to: {filepath}")
    if category:
        print(f"   Filtering by category: {category}")
    
    try:
        count = export_parts_to_csv(filepath, category)
        print(f"✅ Successfully exported {count} parts!")
    except Exception as e:
        print(f"❌ Error during export: {e}")
        sys.exit(1)


def cmd_template(filepath):
    """Create a CSV template file."""
    print(f"\n📝 Creating CSV template: {filepath}")
    
    try:
        create_csv_template(filepath)
        print(f"✅ Template created successfully!")
        print(f"\nEdit the file and add your parts, then run:")
        print(f"  python manage_db.py import {filepath}")
    except Exception as e:
        print(f"❌ Error creating template: {e}")
        sys.exit(1)


def cmd_clear():
    """Clear all parts from database."""
    print(f"\n⚠️  WARNING: This will delete ALL parts from the database!")
    response = input("Type 'yes' to confirm: ")
    
    if response.lower() == 'yes':
        count = clear_parts_database()
        print(f"✅ Cleared {count} parts from database.")
    else:
        print("❌ Operation cancelled.")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'stats':
        cmd_stats()
    
    elif command == 'import':
        if len(sys.argv) < 3:
            print("❌ Error: Missing filepath argument")
            print("Usage: python manage_db.py import <filepath>")
            sys.exit(1)
        cmd_import(sys.argv[2])
    
    elif command == 'export':
        if len(sys.argv) < 3:
            print("❌ Error: Missing filepath argument")
            print("Usage: python manage_db.py export <filepath> [category]")
            sys.exit(1)
        category = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_export(sys.argv[2], category)
    
    elif command == 'template':
        if len(sys.argv) < 3:
            print("❌ Error: Missing filepath argument")
            print("Usage: python manage_db.py template <filepath>")
            sys.exit(1)
        cmd_template(sys.argv[2])
    
    elif command == 'clear':
        cmd_clear()
    
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
