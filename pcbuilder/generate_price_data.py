"""Generate realistic price history data for all components"""
import random
from datetime import datetime, timedelta
from .db import list_parts
from .price_tracker import record_price


def generate_realistic_price_history():
    """Generate 90 days of realistic price history for all parts"""
    parts = list_parts()
    now = datetime.now()
    
    print(f"Generating price history for {len(parts)} parts...")
    
    for part in parts:
        part_id = part['id']
        base_price = part['price']
        category = part['category']
        
        # Category-specific volatility (how much prices fluctuate)
        volatility = {
            'CPU': 0.03,      # 3% daily variance
            'GPU': 0.05,      # 5% daily variance (most volatile)
            'Motherboard': 0.02,
            'RAM': 0.04,
            'Storage': 0.03,
            'PSU': 0.02,
            'Case': 0.015,
            'Cooler': 0.02
        }
        
        # Get volatility for this category
        daily_variance = volatility.get(category, 0.025)
        
        # Generate 90 days of price data
        current_price = base_price
        
        for days_ago in range(89, -1, -1):
            timestamp = (now - timedelta(days=days_ago)).isoformat()
            
            # Add some trend patterns
            # Prices generally decrease over time (tech depreciation)
            trend = -0.0005 * (89 - days_ago)  # Gradual decrease
            
            # Add seasonal/cyclical patterns
            cycle = 0.01 * random.choice([-1, 0, 1]) * (1 if days_ago % 7 == 0 else 0)  # Weekly sales
            
            # Random daily fluctuation
            daily_change = random.gauss(0, daily_variance)
            
            # Calculate new price
            price_multiplier = 1 + trend + cycle + daily_change
            current_price = current_price * price_multiplier
            
            # Ensure price doesn't go too low or too high
            min_price = base_price * 0.7  # Don't drop below 70% of original
            max_price = base_price * 1.3  # Don't go above 130% of original
            current_price = max(min_price, min(max_price, current_price))
            
            # Record the price
            record_price(part_id, round(current_price, 2), timestamp)
        
        print(f"  ✓ Generated data for {part['name']}")
    
    print(f"\n✅ Successfully generated 90 days of price data for {len(parts)} parts!")


if __name__ == "__main__":
    generate_realistic_price_history()
