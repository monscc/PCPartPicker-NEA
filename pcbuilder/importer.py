"""
Database import/export tools for PC Part Picker.

Provides functionality to:
- Import parts from CSV files
- Export parts to CSV files
- Clear database
- Get statistics
- Create CSV templates
"""

import csv
import sqlite3
from pathlib import Path
from typing import Optional, Dict, List, Any


def get_db_connection():
    """Get a connection to the database."""
    conn = sqlite3.connect("pcbuilder.db")
    conn.row_factory = sqlite3.Row
    return conn


def import_parts_from_csv(csv_path: str) -> int:
    """
    Import parts from a CSV file into the database.
    
    Expected CSV columns:
    - id (required)
    - name (required)
    - category (required)
    - price (required)
    - All other columns are treated as attributes
    
    Returns:
        Number of parts imported
    """
    from pcbuilder.db import init_db
    
    # Ensure database exists
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Extract required fields
            part_id = row.get('id', '').strip()
            name = row.get('name', '').strip()
            category = row.get('category', '').strip()
            
            try:
                price = float(row.get('price', 0))
            except ValueError:
                print(f"Warning: Invalid price for {name}, skipping...")
                continue
            
            if not all([part_id, name, category]):
                print(f"Warning: Missing required fields for row, skipping...")
                continue
            
            # Build attributes dict from remaining columns
            attributes = {}
            for key, value in row.items():
                if key not in ['id', 'name', 'category', 'price'] and value:
                    # Convert to string and strip whitespace
                    value_str = str(value).strip() if value else ''
                    if value_str:  # Only add non-empty values
                        # Try to convert to number if possible
                        try:
                            if '.' in value_str:
                                attributes[key] = float(value_str)
                            else:
                                attributes[key] = int(value_str)
                        except ValueError:
                            attributes[key] = value_str
            
            # Convert attributes to JSON string
            import json
            attributes_json = json.dumps(attributes)
            
            # Insert or replace part
            cursor.execute("""
                INSERT OR REPLACE INTO parts (id, name, category, price, attributes)
                VALUES (?, ?, ?, ?, ?)
            """, (part_id, name, category, price, attributes_json))
            
            imported_count += 1
    
    conn.commit()
    conn.close()
    
    return imported_count


def export_parts_to_csv(csv_path: str, category: Optional[str] = None) -> int:
    """
    Export parts from database to a CSV file.
    
    Args:
        csv_path: Path to output CSV file
        category: Optional category filter (e.g., "CPU", "GPU")
    
    Returns:
        Number of parts exported
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM parts WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM parts")
    
    rows = cursor.fetchall()
    
    if not rows:
        conn.close()
        return 0
    
    # Collect all possible attribute keys
    import json
    all_keys = set(['id', 'name', 'category', 'price'])
    for row in rows:
        attributes = json.loads(row['attributes'])
        all_keys.update(attributes.keys())
    
    # Sort keys for consistent column order
    fieldnames = ['id', 'name', 'category', 'price'] + sorted(all_keys - {'id', 'name', 'category', 'price'})
    
    # Write CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            attributes = json.loads(row['attributes'])
            
            # Build output row
            output_row = {
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'price': row['price']
            }
            output_row.update(attributes)
            
            writer.writerow(output_row)
    
    conn.close()
    return len(rows)


def clear_parts_database() -> int:
    """
    Clear all parts from the database.
    
    Returns:
        Number of parts deleted
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM parts")
    count = cursor.fetchone()[0]
    
    cursor.execute("DELETE FROM parts")
    conn.commit()
    conn.close()
    
    return count


def get_part_statistics() -> Dict[str, Any]:
    """
    Get statistics about parts in the database.
    
    Returns:
        Dictionary with:
        - total_parts: Total number of parts
        - by_category: Dictionary of category -> count
        - price_min: Minimum price
        - price_max: Maximum price
        - price_avg: Average price
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total parts
    cursor.execute("SELECT COUNT(*) FROM parts")
    total_parts = cursor.fetchone()[0]
    
    stats = {
        'total_parts': total_parts,
        'by_category': {},
        'price_min': 0,
        'price_max': 0,
        'price_avg': 0
    }
    
    if total_parts == 0:
        conn.close()
        return stats
    
    # Parts by category
    cursor.execute("SELECT category, COUNT(*) as count FROM parts GROUP BY category")
    for row in cursor.fetchall():
        stats['by_category'][row['category']] = row['count']
    
    # Price statistics
    cursor.execute("SELECT MIN(price) as min, MAX(price) as max, AVG(price) as avg FROM parts")
    row = cursor.fetchone()
    stats['price_min'] = row['min']
    stats['price_max'] = row['max']
    stats['price_avg'] = row['avg']
    
    conn.close()
    return stats


def create_csv_template(csv_path: str):
    """
    Create a CSV template file with example data.
    
    Args:
        csv_path: Path to output CSV file
    """
    fieldnames = [
        'id', 'name', 'category', 'price',
        'socket', 'power_draw', 'cores', 'threads',
        'form_factor', 'memory_type', 'memory_slots',
        'gpu_length', 'case_max_gpu_length',
        'wattage', 'efficiency',
        'cooler_height', 'supported_sockets',
        'capacity', 'interface'
    ]
    
    examples = [
        {
            'id': 'cpu-example',
            'name': 'Example CPU',
            'category': 'CPU',
            'price': '199.99',
            'socket': 'LGA1700',
            'power_draw': '125',
            'cores': '8',
            'threads': '16'
        },
        {
            'id': 'mobo-example',
            'name': 'Example Motherboard',
            'category': 'Motherboard',
            'price': '149.99',
            'socket': 'LGA1700',
            'form_factor': 'ATX',
            'memory_type': 'DDR4',
            'memory_slots': '4'
        }
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(examples)
    
    print(f"Created template with {len(examples)} example rows")
