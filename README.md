# PC Part Picker - NEA Project

A Python-based PC part picker application for Computer Science NEA, built with Tkinter GUI and SQLite database.

## Features

### ✅ Implemented
1. **PC Builder** - Interactive component selection with real-time compatibility checking
2. **User Account System** - Secure registration/login with SHA256 password hashing
3. **Build Saving & Loading** - Persistent storage of custom PC builds
4. **Price Tracker** - Historical price tracking with matplotlib charts
5. **Compatibility Engine** - 6+ validation rules (CPU socket, RAM type, PSU wattage, form factors, GPU clearance)
6. **GBP Currency** - All prices displayed in British Pounds (£)
7. **Database Management** - CSV import/export tools for easy data population

### 🔄 Planned
- User settings and UI theme customization
- PyInstaller packaging for standalone .exe distribution
- Expanded parts database (50-200+ components)

## Tech Stack

- **Language**: Python 3.12+
- **GUI**: Tkinter (built-in)
- **Database**: SQLite3 (built-in)
- **Charting**: matplotlib
- **Testing**: pytest

## Project Structure

```
PCPartPicker/
├── pcbuilder/              # Main package
│   ├── __init__.py
│   ├── models.py          # Data structures (Part, Build)
│   ├── db.py              # Database layer
│   ├── compat.py          # Compatibility checking engine
│   ├── accounts.py        # User authentication
│   ├── price_tracker.py   # Price history tracking
│   ├── importer.py        # CSV import/export tools
│   └── ui/                # GUI components
│       ├── app.py         # Main application window
│       └── views/
│           ├── login_frame.py    # Login/register screen
│           ├── main_frame.py     # Tabbed interface
│           ├── builder_tab.py    # PC builder
│           ├── builds_tab.py     # Saved builds viewer
│           └── tracker_tab.py    # Price charts
├── tests/                 # Automated tests (14 tests)
│   ├── test_compat.py
│   ├── test_db.py
│   ├── test_accounts.py
│   ├── test_builds.py
│   └── test_price_tracker.py
├── data/
│   └── sample_parts.json  # 16 UK components with GBP pricing
├── pcbuilder.db           # SQLite database (auto-generated)
├── run_gui.py             # GUI launcher
├── manage_db.py           # Database management CLI
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── DEVELOPMENT_LOG.md     # NEA evidence documentation
├── TESTING_CHECKLIST.md   # Testing guide
├── DATABASE_GUIDE.md      # Data sourcing guide
├── QUICK_IMPORT_GUIDE.md  # Copy-paste ready UK parts
└── GBP_UPDATE_SUMMARY.md  # Currency conversion details
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run GUI
```bash
python run_gui.py
```

### 3. First Launch
- Sample data (16 UK parts) loads automatically if database is empty
- Create an account (username min 3 chars, password min 6 chars)
- Start building PCs in the "Build PC" tab

## Database Management

### View Statistics
```bash
python manage_db.py stats
```

### Create CSV Template
```bash
python manage_db.py template data/my_parts.csv
```

### Import Parts from CSV
```bash
python manage_db.py import data/my_parts.csv
```

### Export Parts to CSV
```bash
python manage_db.py export data/output.csv
```

### Clear All Parts
```bash
python manage_db.py clear
```

## Testing

Run all automated tests:
```bash
pytest -v
```

Current status: **14/14 tests passing** ✅

## Compatibility Rules

The compatibility engine checks:
1. **CPU ↔ Motherboard Socket** - LGA1700, AM4, AM5 matching
2. **RAM ↔ Motherboard Type** - DDR4 vs DDR5 matching
3. **RAM ↔ Motherboard Slots** - Memory slot count validation
4. **Motherboard ↔ Case** - ATX, micro-ATX, mini-ITX form factors
5. **GPU ↔ Case** - GPU length clearance (mm)
6. **PSU Wattage** - Total power draw + 25% headroom

## UK Parts Database

**Current**: 16 components (2 per category)
- CPUs: Intel i5-12400F, AMD Ryzen 5 5600X
- Motherboards: LGA1700, AM4
- RAM: DDR4, DDR5 kits
- GPUs: RTX 4060, RX 7600
- PSUs: 550W, 750W
- Cases: Mid-tower ATX
- Storage: NVMe, SATA SSDs
- Coolers: Air, AIO

**Pricing**: £29.99 - £289.99 (accurate to UK market Oct 2025)

**Expand**: See `QUICK_IMPORT_GUIDE.md` for 50+ copy-paste ready UK components, or `DATABASE_GUIDE.md` for sourcing from Overclockers/Scan/Amazon UK.

## Currency Format

All prices displayed in **GBP (£)**:
- Builder tab: Real-time totals with £ symbol
- Saved builds: Price display in £
- Price tracker: Chart axis labels in £
- Sample data: Realistic UK market prices

## NEA Documentation

For Computer Science NEA evidence:
- `DEVELOPMENT_LOG.md` - 400+ lines of development process documentation
- `TESTING_CHECKLIST.md` - Comprehensive testing guide
- `DATABASE_GUIDE.md` - Research process for UK component data
- `GBP_UPDATE_SUMMARY.md` - Localization decisions

## License

Educational project for Computer Science NEA.
