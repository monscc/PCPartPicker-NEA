# ✅ You're All Set for Manual Data Collection!

## What Just Happened

I've created a complete manual data collection system for you:

✅ **Template Created**: `data/manual_entry.csv`  
✅ **Tool Created**: `manual_collector.py`  
✅ **8 Example Rows**: Already filled in as a guide  
✅ **File Opened**: Should be open in Excel/your CSV editor now

---

## 🎯 Your Workflow (Start Now!)

### 1. Open the Template
The file `data/manual_entry.csv` should be open. If not:
```powershell
explorer data\manual_entry.csv
```

### 2. Delete Example Rows
- Keep the header row (first row with column names)
- Delete rows 2-9 (the examples)
- Start adding your own data

### 3. Visit UK Retailers

**Recommended sites**:
- 🌐 **Overclockers UK**: overclockers.co.uk
- 🌐 **Scan Computers**: scan.co.uk
- 🌐 **Amazon UK**: amazon.co.uk
- 🌐 **CCL Online**: cclonline.com

### 4. Collect Data for Each Component

**Example - Finding a CPU**:

1. Go to Overclockers UK → Components → Processors
2. Click on "Intel Core i7-13700K"
3. Note the details:
   - **Name**: Intel Core i7-13700K
   - **Price**: £379.99 → Enter as `379.99` (no £ symbol!)
   - **Socket**: LGA1700
   - **Cores**: 16
   - **Threads**: 24
   - **TDP**: 125W

4. Add to CSV:
```csv
cpu-i7-13700k,Intel Core i7-13700K,CPU,379.99,Overclockers UK,https://overclockers.co.uk/...,LGA1700,125,16,24
```

### 5. Repeat for All Categories

**Target**: 50-60 components total

- [ ] **CPUs**: 8-10 (Intel i3/i5/i7, AMD Ryzen 5/7)
- [ ] **Motherboards**: 8-10 (LGA1700, AM4, AM5 - mix ATX/micro-ATX)
- [ ] **RAM**: 6-8 (DDR4 and DDR5, 16GB and 32GB kits)
- [ ] **GPUs**: 8-10 (RTX 4060/4070, RX 7600/7700)
- [ ] **PSUs**: 5-6 (550W to 850W, Bronze/Gold)
- [ ] **Cases**: 3-4 (Different sizes)
- [ ] **Storage**: 4-5 (NVMe SSDs, 500GB to 2TB)
- [ ] **Coolers**: 3-4 (Air and AIO liquid coolers)

---

## 📋 Quick Reference: Required Columns

**Every component needs**:
- `id` - Unique identifier (e.g., `cpu-i5-12400f`)
- `name` - Full product name
- `category` - CPU, Motherboard, RAM, GPU, PSU, Case, Storage, or Cooler
- `price` - Numeric only, no £ symbol (e.g., `159.99`)

**Category-specific attributes**:

| Category    | Important Attributes |
|-------------|---------------------|
| CPU         | socket, power_draw, cores, threads |
| Motherboard | socket, form_factor, memory_type, memory_slots |
| RAM         | memory_type, sticks, speed |
| GPU         | power_draw, gpu_length, memory |
| PSU         | wattage, efficiency |
| Case        | mobo_support, case_max_gpu_length |
| Storage     | capacity, interface |
| Cooler      | supported_sockets, type |

---

## 💡 Pro Tips

### Creating Good IDs
- Lowercase with hyphens
- Include category prefix
- Keep it short but descriptive
- Examples:
  - `cpu-i5-12400f`
  - `mobo-b660m-pro`
  - `gpu-rtx4060`
  - `ram-vengeance-16gb`

### Finding Specifications
- Look for "Specifications" or "Tech Specs" tab on product pages
- Common locations:
  - CPU: Socket, Cores, TDP (power)
  - Motherboard: Socket, Form Factor, RAM Type
  - GPU: Length, TDP, VRAM
  - PSU: Wattage, Efficiency Rating

### Pricing
- **Remove £ symbol** - just the number
- Include pence: `159.99` not `159`
- If sale price available, use current price

### Save Frequently!
- Save after every 5-10 components
- Backup the file occasionally
- CSV files are easy to corrupt if Excel crashes

---

## ✅ When You're Done Collecting

### 1. Validate Your Data
```powershell
python manual_collector.py --validate data/manual_entry.csv
```

This checks:
- All required columns present
- No missing data in required fields
- Prices are valid numbers
- Proper formatting

### 2. Import to Database
```powershell
python manage_db.py import data/manual_entry.csv
```

### 3. Check Database
```powershell
python manage_db.py stats
```

Should show your new components!

### 4. Test in GUI
```powershell
python run_gui.py
```

All your components should appear in the dropdowns!

---

## ⏱️ Time Estimate

**Quick session** (30 components):
- 10 CPUs: 10 minutes
- 8 Motherboards: 8 minutes
- 6 RAM kits: 6 minutes
- 6 GPUs: 6 minutes
- **Total**: ~30-45 minutes

**Full session** (60 components):
- Complete coverage of all categories
- **Total**: ~2-3 hours

**Recommendation**: Do it in 2-3 sessions:
- Session 1: CPUs + Motherboards (30 min)
- Session 2: GPUs + RAM + PSUs (45 min)
- Session 3: Cases + Storage + Coolers (30 min)

---

## 🆘 Troubleshooting

### "CSV validation failed"
- Check for missing commas
- Ensure prices are numbers (no £)
- Make sure required columns (id, name, category, price) are filled

### "Import failed"
- Run validation first: `python manual_collector.py --validate data/manual_entry.csv`
- Check error message for specific row
- Fix and try again

### "Components not showing in GUI"
- Check import was successful: `python manage_db.py stats`
- Make sure category names match exactly (case-sensitive)
- Valid categories: CPU, Motherboard, RAM, GPU, PSU, Case, Storage, Cooler

---

## 📊 Example Data Collection Session

Here's what 10 minutes of work looks like:

**Visit Overclockers UK → Processors**:
1. Intel i5-12400F - £159.99 → Add to CSV
2. Intel i5-13600K - £289.99 → Add to CSV
3. AMD Ryzen 5 5600X - £149.99 → Add to CSV
4. AMD Ryzen 7 7800X3D - £429.99 → Add to CSV

**Result**: 4 CPUs in ~10 minutes

Repeat for each category!

---

## 🎯 Current Status

- ✅ Template created with 8 examples
- ✅ `manual_collector.py` tool ready
- ✅ Instructions displayed
- ✅ CSV file should be open in your editor

**Next Action**: Start adding UK components to `data/manual_entry.csv`!

---

## 📝 For Your NEA Documentation

When you write up your NEA, include:

**Data Collection Section**:
```
I collected real UK component pricing data from multiple retailers
to populate my PC Part Picker database. 

Data Collection Method: Manual research and recording
Sources:
- Overclockers UK: [X] products
- Scan Computers: [X] products  
- Amazon UK: [X] products

Total components collected: [X]
Date collected: October 2025
Price range: £[min] - £[max]
Currency: GBP (£)

This manual approach ensured:
- Accurate, up-to-date UK pricing
- Proper attribution of sources
- Respect for retailer terms of service
- High quality, verified data

[Include screenshot of CSV file]
[Include screenshot of retailer product pages]
```

---

## 🚀 Ready to Start?

1. **Open**: `data/manual_entry.csv` (should already be open)
2. **Delete**: Example rows 2-9 (keep header!)
3. **Visit**: overclockers.co.uk or scan.co.uk
4. **Collect**: Start with CPUs, then move through categories
5. **Save**: After every 5-10 components
6. **Import**: When ready, use `python manage_db.py import data/manual_entry.csv`

**Goal**: 50-60 UK components for a comprehensive NEA project database!

Good luck! Let me know if you need any help along the way! 🎉
