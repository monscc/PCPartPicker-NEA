"""
Web scraper for UK PC component prices.

IMPORTANT LEGAL NOTICE:
- This code is for EDUCATIONAL purposes only (Computer Science NEA)
- Always respect website Terms of Service and robots.txt
- Add appropriate delays between requests (rate limiting)
- Do not use for commercial purposes
- Consider manual data collection as an alternative

Before using this scraper:
1. Check the target website's Terms of Service
2. Check robots.txt (e.g., https://www.overclockers.co.uk/robots.txt)
3. Add delays between requests (time.sleep)
4. Use appropriate User-Agent
5. Handle errors gracefully

For NEA: Manual data collection may be more appropriate and is completely legal.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import csv
from typing import List, Dict, Optional
from datetime import datetime


class PCComponentScraper:
    """
    Base class for scraping PC component prices from UK retailers.
    
    Usage:
        scraper = PCComponentScraper()
        products = scraper.scrape_search("RTX 4060", max_results=5)
    """
    
    def __init__(self, delay_seconds: float = 2.0):
        """
        Initialize scraper with rate limiting.
        
        Args:
            delay_seconds: Delay between requests (minimum 2 seconds recommended)
        """
        self.delay = delay_seconds
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Educational Project - PC Part Picker NEA)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9',
        }
    
    def _rate_limit(self):
        """Add delay to respect rate limiting."""
        time.sleep(self.delay)
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make HTTP request with error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            Response object or None if error
        """
        self._rate_limit()
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _extract_price(self, price_text: str) -> Optional[float]:
        """
        Extract numeric price from text like "£159.99".
        
        Args:
            price_text: Price string with currency symbol
            
        Returns:
            Numeric price or None if parsing fails
        """
        try:
            # Remove £, €, $, commas, and whitespace
            price_clean = price_text.replace('£', '').replace('€', '').replace('$', '')
            price_clean = price_clean.replace(',', '').strip()
            return float(price_clean)
        except (ValueError, AttributeError):
            return None
    
    def scrape_search(self, search_term: str, max_results: int = 10) -> List[Dict]:
        """
        Scrape search results for a given term.
        
        This is a template method - override in subclass for specific retailer.
        
        Args:
            search_term: Product to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of product dictionaries
        """
        raise NotImplementedError("Override in subclass for specific retailer")
    
    def save_to_csv(self, products: List[Dict], filename: str):
        """
        Save scraped products to CSV file.
        
        Args:
            products: List of product dictionaries
            filename: Output CSV filename
        """
        if not products:
            print("No products to save")
            return
        
        # Determine all possible keys
        all_keys = set()
        for product in products:
            all_keys.update(product.keys())
        
        fieldnames = ['id', 'name', 'category', 'price', 'source', 'url'] + \
                     sorted(all_keys - {'id', 'name', 'category', 'price', 'source', 'url'})
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(products)
        
        print(f"Saved {len(products)} products to {filename}")


class OverclockersScraper(PCComponentScraper):
    """
    Scraper for Overclockers UK.
    
    WARNING: This is a TEMPLATE only!
    - HTML structure may change
    - CSS selectors are placeholders
    - Check Overclockers' Terms of Service before use
    - Check robots.txt
    
    For NEA: Consider manual data collection instead.
    """
    
    BASE_URL = "https://www.overclockers.co.uk"
    
    def scrape_search(self, search_term: str, max_results: int = 10) -> List[Dict]:
        """
        Scrape Overclockers UK search results.
        
        NOTE: This is a PLACEHOLDER implementation!
        The actual HTML structure will differ and you'll need to:
        1. Inspect the page with browser DevTools
        2. Find correct CSS selectors
        3. Test with small sample first
        """
        url = f"{self.BASE_URL}/search?query={search_term.replace(' ', '+')}"
        
        response = self._make_request(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'lxml')
        products = []
        
        # PLACEHOLDER SELECTORS - WILL NOT WORK!
        # You need to inspect actual HTML and update these
        product_items = soup.find_all('div', class_='productlist-item', limit=max_results)
        
        for item in product_items:
            try:
                # Extract product name
                name_elem = item.find('h3', class_='product-title')
                name = name_elem.text.strip() if name_elem else None
                
                # Extract price
                price_elem = item.find('span', class_='price')
                price_text = price_elem.text.strip() if price_elem else None
                price = self._extract_price(price_text) if price_text else None
                
                # Extract product URL
                link_elem = item.find('a', href=True)
                product_url = self.BASE_URL + link_elem['href'] if link_elem else None
                
                if name and price:
                    # Generate ID from name
                    product_id = name.lower().replace(' ', '-')[:50]
                    
                    products.append({
                        'id': product_id,
                        'name': name,
                        'price': price,
                        'source': 'Overclockers UK',
                        'url': product_url,
                        'scraped_at': datetime.now().isoformat()
                    })
            
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
        
        return products


class ManualDataCollector:
    """
    Helper class for manual data collection (RECOMMENDED for NEA).
    
    Instead of scraping, this provides utilities for manually entering data.
    """
    
    @staticmethod
    def create_entry_template(filename: str):
        """
        Create a CSV template for manual data entry.
        
        Args:
            filename: Output CSV filename
        """
        headers = [
            'id', 'name', 'category', 'price', 'source', 'url',
            'socket', 'power_draw', 'cores', 'threads',
            'form_factor', 'memory_type', 'memory_slots',
            'gpu_length', 'wattage', 'efficiency',
            'capacity', 'interface', 'mobo_support',
            'case_max_gpu_length', 'supported_sockets', 'type'
        ]
        
        # Example rows
        examples = [
            {
                'id': 'cpu-example',
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
            {
                'id': 'gpu-example',
                'name': 'NVIDIA GeForce RTX 4060 8GB',
                'category': 'GPU',
                'price': '289.99',
                'source': 'Scan UK',
                'url': 'https://www.scan.co.uk/...',
                'power_draw': '115',
                'gpu_length': '244'
            }
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(examples)
        
        print(f"Created template: {filename}")
        print("Open in Excel/Google Sheets and fill in your data!")
    
    @staticmethod
    def validate_csv(filename: str) -> bool:
        """
        Validate CSV file has required columns and data.
        
        Args:
            filename: CSV file to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_cols = ['id', 'name', 'category', 'price']
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                # Check required columns
                if not all(col in headers for col in required_cols):
                    print(f"ERROR: Missing required columns. Need: {required_cols}")
                    return False
                
                # Check each row
                row_count = 0
                for i, row in enumerate(reader, start=2):
                    row_count += 1
                    
                    # Check required fields not empty
                    for col in required_cols:
                        if not row.get(col, '').strip():
                            print(f"ERROR: Row {i} missing value for '{col}'")
                            return False
                    
                    # Check price is numeric
                    try:
                        float(row['price'])
                    except ValueError:
                        print(f"ERROR: Row {i} has invalid price: {row['price']}")
                        return False
                
                print(f"✓ CSV valid: {row_count} rows")
                return True
        
        except FileNotFoundError:
            print(f"ERROR: File not found: {filename}")
            return False
        except Exception as e:
            print(f"ERROR: {e}")
            return False


# Example usage
def example_manual_collection():
    """
    Example: Manual data collection workflow (RECOMMENDED).
    """
    print("=" * 60)
    print("RECOMMENDED: Manual Data Collection")
    print("=" * 60)
    
    # Create template
    collector = ManualDataCollector()
    collector.create_entry_template("data/manual_entry.csv")
    
    print("\nNext steps:")
    print("1. Open data/manual_entry.csv in Excel or Google Sheets")
    print("2. Visit UK retailers (Overclockers, Scan, Amazon UK)")
    print("3. For each product:")
    print("   - Copy product name")
    print("   - Copy current price (remove £ symbol)")
    print("   - Copy specifications")
    print("   - Paste into CSV")
    print("4. Save CSV and import:")
    print("   python manage_db.py import data/manual_entry.csv")


def example_web_scraping():
    """
    Example: Web scraping workflow (ADVANCED - check legal first!).
    """
    print("=" * 60)
    print("ADVANCED: Web Scraping")
    print("=" * 60)
    print("\nWARNING: Before proceeding:")
    print("1. Check website Terms of Service")
    print("2. Check robots.txt")
    print("3. Consider if manual collection is better")
    print()
    
    # Create scraper (TEMPLATE ONLY - WILL NOT WORK!)
    scraper = OverclockersScraper(delay_seconds=2.0)
    
    # Search for products
    print("Searching for 'RTX 4060'...")
    products = scraper.scrape_search("RTX 4060", max_results=5)
    
    if products:
        print(f"\nFound {len(products)} products:")
        for p in products:
            print(f"  {p['name']}: £{p['price']:.2f}")
        
        # Save to CSV
        scraper.save_to_csv(products, "data/scraped_gpus.csv")
    else:
        print("No products found (scraper needs customization!)")


if __name__ == '__main__':
    print("PC Component Price Data Collection")
    print()
    print("Choose method:")
    print("1. Manual collection (RECOMMENDED for NEA)")
    print("2. Web scraping (requires customization & legal checks)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        example_manual_collection()
    elif choice == '2':
        example_web_scraping()
    else:
        print("Invalid choice")
