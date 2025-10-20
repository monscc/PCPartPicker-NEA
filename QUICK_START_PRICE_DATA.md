# 🎯 Quick Start: Getting Real Price Data

## Your Options (Ranked by Ease)

### ⭐ **Option 1: Manual Collection** (RECOMMENDED - 2-3 hours)
**Best for**: NEA projects, legal safety, learning research skills

**Pros**: 
- ✅ 100% legal and ethical
- ✅ No technical issues
- ✅ Shows thorough research for NEA
- ✅ Complete control over data quality

**Cons**:
- ⏱️ Takes 2-3 hours for 50-100 components

👉 **[Jump to Manual Collection Guide](#manual-collection)**

---

### ⚙️ **Option 2: Web Scraping** (ADVANCED - requires setup)
**Best for**: Automated price updates, technical demonstration

**Pros**:
- 🤖 Automated data collection
- 📊 Can track price changes over time
- 💻 Demonstrates coding skills

**Cons**:
- ⚠️ Must respect Terms of Service & robots.txt
- 🔧 Requires library installation
- 🐛 Website changes can break scraper
- ⏱️ Still takes time to customize

👉 **[Jump to Web Scraping Guide](#web-scraping)**

---

## Manual Collection

### Step 1: Create Entry Template

```powershell
python scraper.py
# Choose option 1
```

This creates `data/manual_entry.csv` with example rows.

### Step 2: Open in Excel/Sheets

- Open `data/manual_entry.csv` in Excel or Google Sheets
- You'll see columns: id, name, category, price, source, url, etc.

### Step 3: Browse UK Retailers

Visit these trusted sites:
1. **Overclockers UK** - overclockers.co.uk
2. **Scan Computers** - scan.co.uk
3. **Amazon UK** - amazon.co.uk
4. **CCL Online** - cclonline.com

### Step 4: Collect Component Data

#### Example: Collecting a CPU

1. Go to Overclockers UK → Processors → Intel
2. Find: **Intel Core i5-12400F**
3. Note the details:
   - **Price**: £159.99
   - **Socket**: LGA1700
   - **Cores**: 6
   - **Threads**: 12
   - **TDP**: 117W

4. Add to CSV:
```csv
cpu-i5-12400f,Intel Core i5-12400F,CPU,159.99,Overclockers UK,https://overclockers.co.uk/...,LGA1700,117,6,12
```

**Key**: Remove the £ symbol from price (just enter 159.99)

### Step 5: Repeat for Each Category

Suggested quantities:
- **CPUs**: 8-10 (mix Intel/AMD, different sockets)
- **Motherboards**: 8-10 (various sockets and form factors)
- **RAM**: 6-8 (DDR4 and DDR5, different capacities)
- **GPUs**: 8-10 (budget to high-end)
- **PSUs**: 5-6 (different wattages)
- **Cases**: 3-4 (different sizes)
- **Storage**: 4-5 (NVMe and SATA)
- **Coolers**: 3-4 (air and AIO)

**Total**: 50-60 components = **2-3 hours of work**

### Step 6: Import to Database

```powershell
# Validate your CSV first
python -c "from scraper import ManualDataCollector; ManualDataCollector.validate_csv('data/manual_entry.csv')"

# If valid, import
python manage_db.py import data/manual_entry.csv

# Check results
python manage_db.py stats
```

### Step 7: Test in GUI

```powershell
python run_gui.py
```

All your components should appear in the dropdowns!

---

## Web Scraping

### Step 1: Install Libraries

```powershell
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast parser

### Step 2: Check Legal Compliance

Before scraping ANY website:

1. **Check Terms of Service**
   - Visit retailer website
   - Find "Terms & Conditions" or "Terms of Service"
   - Look for clauses about automated access/bots
   - Some sites explicitly prohibit scraping

2. **Check robots.txt**
   ```
   https://www.overclockers.co.uk/robots.txt
   https://www.scan.co.uk/robots.txt
   https://www.amazon.co.uk/robots.txt
   ```
   - Look for `Disallow:` rules
   - Respect crawl delays if specified

3. **Legal for Educational Use?**
   - NEA projects may fall under "fair use"
   - BUT: Always better to ask permission or use manual collection
   - Document your research and ethical considerations

### Step 3: Customize Scraper

The `scraper.py` file contains **TEMPLATE CODE** that won't work as-is.

You need to:

1. **Inspect the website HTML**
   - Open retailer website in browser
   - Right-click → "Inspect" (Chrome/Edge DevTools)
   - Find product listings
   - Note CSS classes for: name, price, link

2. **Update CSS selectors in code**
   ```python
   # Example - update these lines in scraper.py
   product_items = soup.find_all('div', class_='ACTUAL-CLASS-NAME')
   name_elem = item.find('h3', class_='ACTUAL-NAME-CLASS')
   price_elem = item.find('span', class_='ACTUAL-PRICE-CLASS')
   ```

3. **Test on ONE product first**
   ```python
   products = scraper.scrape_search("RTX 4060", max_results=1)
   ```

### Step 4: Run Scraper

```powershell
python scraper.py
# Choose option 2
```

### Step 5: Import Scraped Data

```powershell
python manage_db.py import data/scraped_gpus.csv
python manage_db.py stats
```

---

## Recommended Workflow for NEA

### Week 1: Manual Collection (Primary Data)

1. **Day 1-2**: Collect 50 components manually (2-3 hours)
   - Document sources in CSV
   - Take screenshots of retailer pages
   - Note data collection date

2. **Day 3**: Import and test
   - Import CSV to database
   - Test in GUI
   - Verify compatibility rules work

### Week 2: Web Scraping (Optional Technical Demo)

1. **Day 1**: Research legal compliance
   - Check Terms of Service
   - Check robots.txt
   - Document findings

2. **Day 2-3**: Create scraper (if legal)
   - Customize scraper.py for one retailer
   - Test with small sample
   - Add error handling

3. **Day 4**: Use scraper for updates
   - Update prices for existing components
   - Document in NEA as "technical extension"

### NEA Documentation

Include in your writeup:

**Research Section**:
```
Data Collection Method: Manual browsing and recording

I researched current UK component prices from the following retailers:
- Overclockers UK: 25 products
- Scan Computers: 15 products
- Amazon UK: 10 products

Date collected: October 2025
Total components: 50
Price range: £29.99 - £549.99

[Include screenshot of retailer product page]
[Include screenshot of your CSV file]
```

**Optional Technical Section** (if you add scraping):
```
Price Update Automation:

I created a web scraping module using BeautifulSoup to
automate price updates. Ethical considerations:

1. Checked Overclockers UK Terms of Service
2. Respected robots.txt directives
3. Added 2-second delays between requests
4. Included identifying User-Agent
5. Handled network errors gracefully
6. Used for educational purposes only

[Include code snippet]
[Include scraper output]
```

---

## Quick Reference: UK Retailer Prices

### Current Market Prices (October 2025)

**CPUs**:
- Intel i3-12100F: £89.99
- Intel i5-12400F: £159.99
- Intel i5-13600K: £289.99
- AMD Ryzen 5 5600: £129.99
- AMD Ryzen 5 5600X: £149.99
- AMD Ryzen 7 5700X: £209.99

**GPUs**:
- RTX 4060 8GB: £289.99
- RTX 4060 Ti 8GB: £409.99
- RTX 4070 12GB: £549.99
- RX 6600 8GB: £199.99
- RX 7600 8GB: £249.99
- RX 7700 XT 12GB: £449.99

**Motherboards**:
- B660M Micro-ATX DDR4: £99-120
- B760M Micro-ATX DDR4: £140-170
- B550 ATX DDR4: £130-160
- B650 ATX DDR5: £200-230

**RAM**:
- 16GB (2x8GB) DDR4 3200MHz: £30-40
- 32GB (2x16GB) DDR4 3600MHz: £60-70
- 16GB (2x8GB) DDR5 5600MHz: £60-75
- 32GB (2x16GB) DDR5 6000MHz: £95-110

**PSUs**:
- 550W 80+ Bronze: £40-50
- 650W 80+ Gold: £65-75
- 750W 80+ Gold: £85-95
- 850W 80+ Gold: £110-130

---

## Time Estimates

### Manual Collection:
- **10 CPUs**: 10 minutes
- **10 Motherboards**: 10 minutes
- **8 RAM kits**: 8 minutes
- **10 GPUs**: 10 minutes
- **6 PSUs**: 6 minutes
- **4 Cases**: 5 minutes
- **5 Storage**: 5 minutes
- **4 Coolers**: 5 minutes
- **Total**: ~60 minutes for 57 components

Add ~30-60 minutes for:
- Creating proper IDs
- Filling in attributes
- Validating data
- Formatting CSV

**Grand Total**: 2-3 hours for 50-100 quality components

### Web Scraping:
- **Setup libraries**: 5 minutes
- **Research legal**: 30 minutes
- **Inspect HTML**: 30 minutes
- **Customize scraper**: 1-2 hours
- **Test and debug**: 1-2 hours
- **Run scraper**: 5 minutes
- **Total**: 3-5 hours (but then automated!)

---

## FAQ

**Q: Do I need to scrape for my NEA?**  
A: No! Manual collection is perfectly acceptable and often better. Shows thorough research.

**Q: Is web scraping legal?**  
A: Gray area. Depends on Terms of Service and intended use. For educational NEA projects with proper attribution, generally acceptable. When in doubt, collect manually.

**Q: How many components do I need?**  
A: 
- **Minimum**: 20-30 (adequate)
- **Good**: 50-80 (shows effort)
- **Excellent**: 100+ (comprehensive)

**Q: How often should I update prices?**  
A: For NEA, one-time collection is fine. Optional: Update once per week if you want to demonstrate price tracker functionality.

**Q: Can I use US prices?**  
A: Should use UK prices (GBP) since it's a UK NEA project and your app uses £.

**Q: What if a retailer changes their website?**  
A: This is why manual collection is safer for NEA! Scrapers break when sites change.

---

## Next Steps

Choose your path:

### Path A: Manual Collection (Recommended)
1. Run: `python scraper.py` → Choose option 1
2. Open `data/manual_entry.csv` in Excel
3. Spend 2-3 hours collecting data from UK retailers
4. Import: `python manage_db.py import data/manual_entry.csv`
5. Test: `python run_gui.py`

### Path B: Web Scraping (Advanced)
1. Install: `pip install -r requirements.txt`
2. Research legal compliance for target retailer
3. Customize `scraper.py` with correct CSS selectors
4. Test with 1-2 products first
5. Run full scrape
6. Import and test

**My Recommendation**: Start with Path A (manual). If you finish early and want to add technical flair, try Path B as an extension.

---

Need help? Let me know which path you choose!
