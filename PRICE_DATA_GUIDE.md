# Web Scraping Guide for PC Part Picker

## Overview
This guide explains how to obtain real price data for PC components from UK retailers for your NEA project.

---

## ⚠️ Important Legal & Ethical Considerations

### 1. Website Terms of Service
- **Always** read and respect the Terms of Service of any website you scrape
- Some websites explicitly prohibit automated data collection
- Commercial use may be restricted even if personal use is allowed

### 2. robots.txt
Check the website's `robots.txt` file:
- Example: `https://www.overclockers.co.uk/robots.txt`
- Respect any `Disallow:` directives
- Some sites allow scraping but rate-limit requests

### 3. Rate Limiting
- **Don't** make rapid-fire requests (looks like a DDoS attack)
- Add delays between requests (1-2 seconds minimum)
- Consider caching data instead of repeated scraping
- Use `time.sleep()` between requests

### 4. Fair Use for Educational Projects
For NEA purposes:
- ✅ One-time data collection for academic project
- ✅ Citing sources in documentation
- ✅ Not redistributing scraped data commercially
- ✅ Small sample size (50-200 products, not entire catalog)

### 5. Alternative: Manual Data Entry
If scraping feels legally risky:
- Manually browse retailer websites
- Copy prices into CSV file
- Cite sources in documentation
- **This is completely legal and often easier!**

---

## Option 1: Web Scraping with Python

### Required Libraries

Install these packages:
```bash
pip install requests beautifulsoup4 lxml
```

Update your `requirements.txt`:
```
pytest
matplotlib
requests
beautifulsoup4
lxml
```

### Basic Scraping Example

```python
import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_overclockers_search(search_term, max_results=10):
    """
    Example scraper for Overclockers UK search results.
    
    WARNING: Check Overclockers' Terms of Service and robots.txt
    before using this in practice!
    """
    # Add delay to be respectful
    time.sleep(2)
    
    # User agent to identify yourself
    headers = {
        'User-Agent': 'Educational Project - PC Part Picker NEA (contact: your.email@example.com)'
    }
    
    # Search URL (may need adjustment based on site structure)
    url = f"https://www.overclockers.co.uk/search?query={search_term}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        products = []
        
        # NOTE: These selectors are EXAMPLES and may not work!
        # You'll need to inspect the actual HTML structure
        for item in soup.find_all('div', class_='product-item', limit=max_results):
            name_elem = item.find('h3', class_='product-name')
            price_elem = item.find('span', class_='product-price')
            
            if name_elem and price_elem:
                name = name_elem.text.strip()
                price_text = price_elem.text.strip()
                
                # Extract numeric price (e.g., "£159.99" -> 159.99)
                price = float(price_text.replace('£', '').replace(',', ''))
                
                products.append({
                    'name': name,
                    'price': price,
                    'source': 'Overclockers UK',
                    'url': url
                })
        
        return products
        
    except requests.RequestException as e:
        print(f"Error scraping: {e}")
        return []

# Example usage
if __name__ == '__main__':
    # Search for graphics cards
    gpus = scrape_overclockers_search("RTX 4060", max_results=5)
    
    for gpu in gpus:
        print(f"{gpu['name']}: £{gpu['price']:.2f}")
```

### Key Points:
1. **Inspect HTML**: Use browser DevTools to find correct CSS selectors
2. **Handle Errors**: Network issues, HTML changes, etc.
3. **Respectful Scraping**: Add delays, identify yourself in User-Agent
4. **Test Small**: Scrape 1-2 items first to verify it works

---

## Option 2: Manual Data Collection (Easiest & Safest)

### Step-by-Step Process

#### 1. Create a Spreadsheet

Open Excel/Google Sheets with columns:
```
ID | Name | Category | Price | Socket | Power | Cores | Threads | ... (other attributes)
```

#### 2. Browse Retailer Websites

Visit these trusted UK retailers:
- **Overclockers UK**: overclockers.co.uk
- **Scan Computers**: scan.co.uk
- **Amazon UK**: amazon.co.uk
- **CCL Online**: cclonline.com
- **Currys PC World**: currys.co.uk

#### 3. Collect Data

For each component:
1. Navigate to product page
2. Copy product name
3. Copy current price
4. Note specifications (socket, wattage, etc.)
5. Paste into spreadsheet

**Example - Intel Core i5-12400F**:
- **Retailer**: Overclockers UK
- **URL**: https://www.overclockers.co.uk/...
- **Price**: £159.99
- **Socket**: LGA1700
- **Cores**: 6
- **Threads**: 12
- **TDP**: 117W

#### 4. Save as CSV

Export your spreadsheet as CSV:
```csv
id,name,category,price,socket,power_draw,cores,threads
cpu-i5-12400f,Intel Core i5-12400F,CPU,159.99,LGA1700,117,6,12
cpu-r5-5600x,AMD Ryzen 5 5600X,CPU,149.99,AM4,65,6,12
```

#### 5. Import to Database

```bash
python manage_db.py import data/uk_parts.csv
```

### Time Estimate
- 50 components: ~2-3 hours
- 100 components: ~4-5 hours
- 200 components: ~8-10 hours

**NEA Consideration**: This is legitimate research and can be documented as evidence of thorough planning.

---

## Option 3: Price Comparison APIs

Some services offer APIs for price data:

### 1. PriceRunner UK (pricerunner.co.uk)
- Price comparison service
- May have API (check their developer docs)
- **Status**: Check if available for educational use

### 2. CamelCamelCamel (Amazon tracker)
- Tracks Amazon UK prices over time
- May have API access
- **Status**: Primarily for Amazon products only

### 3. Google Shopping API
- Aggregates prices from multiple retailers
- Requires API key
- **Status**: May have usage limits/costs

**Reality Check**: Most price comparison APIs are commercial and may not be free for student use.

---

## Option 4: Use Existing Dataset (with Citation)

### PC Part Picker API (pcpartpicker.com)

**Important**: PC Part Picker has a **US-focused** database, but they do have UK pricing.

```python
# NOTE: PC Part Picker does not have a public API
# This is for illustration only - would require web scraping
```

**Pros**: Comprehensive data  
**Cons**: Still requires scraping, mostly US prices

### Kaggle Datasets

Search Kaggle for PC component datasets:
- `kaggle.com/datasets`
- Search terms: "PC components", "computer parts", "hardware prices"

**Pros**: Pre-collected, legal to use with attribution  
**Cons**: May be outdated, might not have UK prices

---

## 🎓 Recommended Approach for NEA

### **Hybrid Method (Best for NEA Evidence)**

1. **Manual Collection** (Primary method)
   - Spend 2-3 hours collecting 50-100 UK components
   - Document sources in spreadsheet
   - Take screenshots of retailer pages
   - **NEA Evidence**: Shows thorough research

2. **Basic Web Scraping** (Secondary/Optional)
   - Create simple scraper for ONE retailer
   - Use it to update prices periodically
   - **NEA Evidence**: Demonstrates technical skill

3. **Historical Data** (For Price Tracker)
   - Manually record prices at different dates, OR
   - Generate realistic random variations, OR
   - Use existing historical data if available

### NEA Documentation

In your documentation, include:

**Research Section**:
```
I researched current UK component prices from the following retailers:
- Overclockers UK: 25 products
- Scan Computers: 15 products  
- Amazon UK: 10 products

Data collection method: Manual browsing and recording
Date collected: October 2025
Prices stored in GBP (£)

[Include screenshot of retailer product page]
[Include screenshot of your CSV/spreadsheet]
```

**Technical Section** (if you add scraping):
```
I created a web scraping module using BeautifulSoup to automate
price updates. Key considerations:
- Respected robots.txt and rate limiting
- Added 2-second delays between requests
- Included User-Agent identification
- Handled network errors gracefully

[Include code snippet]
```

---

## Sample Data Collection Template

### CSV Template for Manual Entry

```csv
id,name,category,price,source,url,socket,power_draw,cores,threads,form_factor,memory_type,memory_slots,gpu_length,wattage,efficiency,capacity,interface,mobo_support,case_max_gpu_length,supported_sockets,type
cpu-i5-12400f,Intel Core i5-12400F,CPU,159.99,Overclockers UK,https://...,LGA1700,117,6,12,,,,,,,,,,,,,
mobo-b660m,MSI B660M PRO-A DDR4,Motherboard,104.99,Scan UK,https://...,LGA1700,,,,,micro-ATX,DDR4,4,,,,,,,,,,
ram-vengeance,Corsair Vengeance 16GB DDR4,RAM,34.99,Amazon UK,https://...,,,,,,,,DDR4,2,,,,,,,,,,
```

### Spreadsheet Columns Explained

**Required for all**:
- `id`: Unique identifier (e.g., cpu-i5-12400f)
- `name`: Full product name
- `category`: CPU, Motherboard, RAM, GPU, PSU, Case, Storage, Cooler
- `price`: Numeric price in GBP (no £ symbol)

**Category-specific attributes**:
- **CPU**: socket, power_draw, cores, threads
- **Motherboard**: socket, form_factor, memory_type, memory_slots
- **RAM**: memory_type, sticks, speed
- **GPU**: power_draw, gpu_length, memory
- **PSU**: wattage, efficiency
- **Case**: mobo_support, case_max_gpu_length
- **Storage**: capacity, interface, power_draw
- **Cooler**: supported_sockets, type

---

## Quick Start: 30 Minutes to 50 Components

### Efficient Data Collection Strategy

1. **CPUs (10 components, 5 minutes)**
   - Go to Overclockers UK → Processors
   - Sort by popularity
   - Pick top 5 Intel + top 5 AMD
   - Record: name, price, socket, cores, TDP

2. **Motherboards (10 components, 5 minutes)**
   - Filter by socket (LGA1700, AM4, AM5)
   - Pick 3-4 of each socket type
   - Record: name, price, socket, form factor, RAM type

3. **RAM (8 components, 3 minutes)**
   - Filter by DDR4 / DDR5
   - Pick 4 of each type
   - Record: name, price, type, capacity, speed

4. **GPUs (10 components, 5 minutes)**
   - Sort by price range
   - Pick 2-3 from each tier (budget/mid/high)
   - Record: name, price, TDP, length

5. **PSUs (5 components, 3 minutes)**
   - Pick range: 550W, 650W, 750W, 850W, 1000W
   - Record: name, price, wattage, efficiency

6. **Cases (3 components, 2 minutes)**
   - Pick 1 mini-ITX, 1 micro-ATX, 1 ATX
   - Record: name, price, form factors, GPU clearance

7. **Storage (2 components, 2 minutes)**
   - 1 NVMe, 1 SATA SSD
   - Record: name, price, capacity, interface

8. **Coolers (2 components, 2 minutes)**
   - 1 air cooler, 1 AIO liquid cooler
   - Record: name, price, socket support

**Total Time**: ~30 minutes for 50 components

---

## Example: Complete Manual Process

### Step 1: Browse Overclockers UK

Navigate to: `https://www.overclockers.co.uk/pc-components/processors-cpus/intel/socket-lga1700`

### Step 2: Record Data

Product: Intel Core i5-12400F
- **Price**: £159.99
- **In Stock**: Yes
- **Specifications**:
  - Socket: LGA1700
  - Cores: 6
  - Threads: 12
  - Base Clock: 2.5 GHz
  - Boost: 4.4 GHz
  - TDP: 117W

### Step 3: Add to CSV

```csv
cpu-i5-12400f,Intel Core i5-12400F,CPU,159.99,LGA1700,117,6,12
```

### Step 4: Repeat 49 more times!

---

## Recommended Final Approach

For your NEA, I recommend:

1. **Week 1**: Manually collect 50-100 UK components (2-3 hours)
2. **Week 2**: Import into database and test GUI
3. **Week 3** (Optional): Add basic scraper for price updates
4. **Week 4**: Document research process with screenshots

This shows:
- ✅ Thorough research
- ✅ Real UK market data
- ✅ Professional data management
- ✅ Technical skills (if you add scraping)
- ✅ No legal concerns

---

## Need Help Getting Started?

Would you like me to:
1. Create a web scraper for a specific UK retailer?
2. Generate a detailed CSV template with 100+ example rows?
3. Create a GUI tool for manually entering component data?
4. Show you how to use an existing dataset from Kaggle?

Let me know which approach interests you most!
