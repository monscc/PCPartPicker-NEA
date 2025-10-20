# Template Builds System - Documentation

## Overview
The PC Part Picker now includes **3 pre-configured template builds** that are available to all users (including guests). This feature helps beginners get started quickly with proven configurations.

## Template Builds

### 1. 💰 Budget Gaming Build (£500-700)
**Description:** Perfect entry-level gaming PC for 1080p gaming and everyday tasks. Great for esports titles and casual gaming on a tight budget.

**Target Components:**
- **CPU:** Intel Core i3-12100F
- **Motherboard:** MSI B660M PRO-A DDR4
- **RAM:** Corsair Vengeance LPX 16GB (2x8GB) DDR4 3200MHz
- **GPU:** AMD Radeon RX 6600 8GB
- **PSU:** Corsair CV550 550W 80+ Bronze
- **Case:** NZXT H510 Compact ATX Mid-Tower
- **Storage:** Samsung 870 EVO 500GB 2.5" SATA SSD
- **Cooler:** Cooler Master Hyper 212 Black Edition

**Use Case:**
- Esports gaming (CS:GO, Valorant, League of Legends)
- 1080p gaming at medium-high settings
- Office work and web browsing
- Students on a budget

---

### 2. 🎮 Mid-Range Performance Build (£800-1200)
**Description:** Excellent all-round gaming PC for 1440p gaming and content creation. Balances performance and value with room for upgrades.

**Target Components:**
- **CPU:** Intel Core i5-12400F
- **Motherboard:** MSI MAG B760M MORTAR WIFI DDR4
- **RAM:** G.Skill Trident Z5 RGB 32GB (2x16GB) DDR5 6000MHz
- **GPU:** NVIDIA GeForce RTX 4060 Ti 8GB
- **PSU:** Corsair RM650e 650W 80+ Gold
- **Case:** Corsair 4000D Airflow ATX Mid-Tower
- **Storage:** Samsung 980 PRO 1TB M.2 NVMe Gen4 SSD
- **Cooler:** be quiet! Dark Rock 4

**Use Case:**
- 1440p gaming at high-ultra settings
- Content creation (video editing, streaming)
- Multitasking and productivity
- VR-ready gaming

---

### 3. 🚀 High-End Enthusiast Build (£1500+)
**Description:** Top-tier gaming and workstation PC for 4K gaming, streaming, and heavy workloads. No compromises on performance.

**Target Components:**
- **CPU:** AMD Ryzen 7 7800X3D
- **Motherboard:** ASUS ROG CROSSHAIR X670E HERO
- **RAM:** G.Skill Trident Z5 RGB 32GB (2x16GB) DDR5 6000MHz
- **GPU:** NVIDIA GeForce RTX 4070 Ti 12GB
- **PSU:** Corsair RM850x 850W 80+ Gold
- **Case:** Lian Li O11 Dynamic EVO
- **Storage:** Samsung 990 PRO 2TB M.2 NVMe Gen4 SSD
- **Cooler:** Noctua NH-D15 chromax.black

**Use Case:**
- 4K gaming at ultra settings
- Professional video editing and 3D rendering
- High-end streaming and content creation
- Competitive gaming with maximum FPS

---

## Features

### Quick Load Buttons (Builder Tab)
Located at the top of the Builder tab, three buttons allow instant loading:
- **💰 Budget** - Loads budget build
- **🎮 Mid-Range** - Loads mid-range build
- **🚀 High-End** - Loads high-end build

**What happens when you click:**
1. Shows confirmation dialog with build details and price
2. If confirmed, replaces current build with template
3. Updates all component dropdowns
4. Displays total price
5. Warns if any components are missing from database

### Template Browser (My Builds Tab)
**Location:** Top of "My Builds" tab

**Features:**
- Lists all 3 templates with names and target prices
- **View button** for each template:
  - Opens detailed window
  - Shows all components and prices
  - Runs compatibility check
  - Allows loading to builder

**Available to:**
- ✅ All users (including guests)
- ✅ No sign-in required to view templates
- ✅ Can load directly to builder

---

## Technical Implementation

### Files Created/Modified

**New File:**
- `pcbuilder/templates.py` (220 lines)
  - `TemplateBuild` class
  - `TEMPLATE_BUILDS` dictionary
  - `get_template_builds()` - Get all templates
  - `get_template_build(id)` - Get specific template
  - `load_template_build(id)` - Resolve template to actual parts
  - `calculate_template_price(id)` - Calculate total cost
  - `get_template_summary(id)` - Get template statistics

**Modified Files:**
- `pcbuilder/ui/views/builder_tab.py`
  - Added template button section
  - Added `_load_template()` method
  - Import template functions

- `pcbuilder/ui/views/builds_tab.py`
  - Added template browser section
  - Added `_view_template()` method
  - Added `_load_template_to_builder()` method

### Key Programming Techniques

#### 1. **Data Encapsulation**
```python
class TemplateBuild:
    """Represents a template PC build"""
    def __init__(self, name, description, target_price, components):
        self.name = name
        self.description = description
        self.target_price = target_price
        self.components = components  # Category -> Part name mapping
```

#### 2. **Name Resolution Algorithm**
```python
def load_template_build(template_id):
    """Resolve template component names to actual part objects"""
    # 1. Try exact name match
    # 2. Try partial/fuzzy match if exact fails
    # 3. Match category to ensure correctness
```

#### 3. **Error Handling**
- Gracefully handles missing components
- Warns users when parts aren't in database
- Allows partial template loading

#### 4. **UI/UX Patterns**
- Confirmation dialogs before replacing builds
- Detailed preview windows
- Real-time price calculation
- Compatibility checking

---

## User Workflows

### Workflow 1: Quick Start (Guest User)
1. Open app → Click "Continue as Guest"
2. See template buttons at top of Builder
3. Click "💰 Budget"
4. Review build details (£169.97 actual with current database)
5. Click "Yes" to load
6. Template loads with available components
7. Can customize further or check compatibility
8. Guest cannot save, but can build and experiment

### Workflow 2: Browse Templates
1. Navigate to "My Builds" tab
2. See template section at top
3. Click "View" on any template
4. Review detailed window:
   - Component list with prices
   - Compatibility check results
   - Total price calculation
5. Click "Load to Builder" to use template
6. Switches to Builder tab with template loaded

### Workflow 3: Template as Starting Point
1. Load template (Budget/Mid-Range/High-End)
2. Customize components:
   - Upgrade GPU for better performance
   - Add more RAM
   - Change case for aesthetics
3. Check compatibility
4. Save custom build (if logged in)

---

## Database Considerations

**Current Limitation:**
The sample database (16 parts) only includes basic components. Many template parts won't be found.

**When template parts are missing:**
- System shows warning dialog
- Lists missing categories
- Loads available parts only
- User can select alternatives

**Solution for Production:**
Import the full `uk_components_complete.csv` (82 parts) to match most template components.

---

## Benefits for NEA Assessment

### 1. **Algorithm Design**
- Fuzzy matching algorithm for part names
- Efficient lookup using dictionaries
- Category-based validation

### 2. **Data Structures**
- Dictionary-based templates
- Nested data structures (components within builds)
- Separation of template definition and resolution

### 3. **User Experience**
- Reduces learning curve for beginners
- Provides proven configurations
- Educational value (shows good component combinations)

### 4. **Extensibility**
Easy to add more templates:
```python
'ultra_budget': TemplateBuild(
    name="🏷️ Ultra Budget Build",
    target_price="£300-400",
    components={...}
)
```

### 5. **Accessibility**
- Available to all users (including guests)
- No authentication barrier
- Instant gratification

---

## Future Enhancements

1. **User-Submitted Templates**
   - Allow premium users to create and share templates
   - Community voting system
   - Featured templates

2. **Dynamic Templates**
   - Update prices in real-time
   - Suggest alternatives when parts out of stock
   - Regional templates (US, EU, UK)

3. **Template Categories**
   - Workstation builds
   - Streaming builds
   - Compact/SFF builds
   - Silent builds

4. **Template Variations**
   - AMD vs Intel variants
   - RGB vs non-RGB options
   - Different storage tiers

5. **Template Analytics**
   - Track most popular templates
   - Measure load success rate
   - User customization patterns

---

## Testing the Feature

### Test Template Loading:
1. Run `python run_gui.py`
2. Click "Continue as Guest"
3. Click "💰 Budget" button
4. Verify confirmation dialog shows build details
5. Click "Yes"
6. Verify components load correctly
7. Check compatibility

### Test Template Browser:
1. Navigate to "My Builds" tab
2. See 3 templates listed
3. Click "View" on "🎮 Mid-Range Performance Build"
4. Verify detailed window opens
5. Check component list
6. Review compatibility results
7. Click "Load to Builder"
8. Verify switch to Builder tab with loaded parts

### Test Missing Parts:
1. Load any template
2. If warning appears, verify:
   - Lists specific missing categories
   - Still loads available parts
   - Allows manual selection of alternatives

---

This template system demonstrates:
- **Practical problem solving** (helping beginners)
- **Algorithm design** (name resolution)
- **Data structures** (nested templates)
- **User interface design** (multiple access points)
- **Error handling** (missing parts)

Perfect for showcasing comprehensive programming skills in your NEA! 🎓✨
