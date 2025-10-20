# Component Filtering System

## Overview
Advanced filtering system with unique filters tailored for each component category, allowing users to narrow down part selections based on specific criteria.

## Features

### 🔍 Filter Button for Each Component
- Every component dropdown has a **"🔍 Filter"** button
- Click to open a dialog with category-specific filters
- Active filter count shown in button: **"🔍 Filter (3)"**

### Unique Filters by Component

#### **CPU Filters**
- ✅ **6+ Cores** - CPUs with 6 or more cores
- ✅ **8+ Cores** - CPUs with 8 or more cores
- ✅ **12+ Cores** - CPUs with 12 or more cores
- ✅ **4.0+ GHz Boost** - High boost clock speeds
- ✅ **Unlocked (K/X)** - Overclockable processors
- ✅ **Integrated Graphics** - CPUs with iGPU

#### **Motherboard Filters**
- ✅ **ATX Size** - Full ATX form factor
- ✅ **Micro-ATX Size** - Smaller mATX boards
- ✅ **Mini-ITX Size** - Compact ITX boards
- ✅ **Built-in WiFi** - Wireless connectivity included
- ✅ **DDR5 Support** - Next-gen memory support
- ✅ **DDR4 Support** - Current-gen memory support

#### **RAM Filters**
- ✅ **16GB+** - 16GB or more capacity
- ✅ **32GB+** - 32GB or more capacity
- ✅ **DDR4** - DDR4 memory type
- ✅ **DDR5** - DDR5 memory type
- ✅ **3200 MHz+** - 3200MHz or faster
- ✅ **3600 MHz+** - 3600MHz or faster
- ✅ **RGB Lighting** - RGB-enabled RAM

#### **GPU Filters**
- ✅ **8GB+ VRAM** - 8GB or more video memory
- ✅ **12GB+ VRAM** - 12GB or more video memory
- ✅ **16GB+ VRAM** - 16GB or more video memory
- ✅ **NVIDIA** - NVIDIA graphics cards
- ✅ **AMD** - AMD graphics cards
- ✅ **Ray Tracing** - RTX or RDNA 3 cards

#### **PSU Filters**
- ✅ **Fully Modular** - All cables removable
- ✅ **Semi-Modular** - Main cables fixed, others removable
- ✅ **Non-Modular** - All cables fixed
- ✅ **650W+** - 650W or higher wattage
- ✅ **750W+** - 750W or higher wattage
- ✅ **850W+** - 850W or higher wattage
- ✅ **80+ Gold** - Gold efficiency rating
- ✅ **80+ Platinum** - Platinum efficiency rating

#### **Case Filters**
- ✅ **ATX Support** - Supports ATX motherboards
- ✅ **Micro-ATX Support** - Supports mATX motherboards
- ✅ **Mini-ITX Support** - Supports ITX motherboards
- ✅ **Tempered Glass** - Glass side panel
- ✅ **RGB Lighting** - Built-in RGB lights
- ✅ **Mesh Front Panel** - Mesh for better airflow

#### **Storage Filters**
- ✅ **SSD** - Solid state drives
- ✅ **HDD** - Hard disk drives
- ✅ **NVMe** - NVMe M.2 interface
- ✅ **SATA** - SATA interface
- ✅ **500GB+** - 500GB or more capacity
- ✅ **1TB+** - 1TB or more capacity
- ✅ **2TB+** - 2TB or more capacity
- ✅ **PCIe 4.0** - Gen4 NVMe drives

#### **Cooler Filters**
- ✅ **Air Cooler** - Traditional tower coolers
- ✅ **AIO Liquid** - All-in-one liquid coolers
- ✅ **120mm** - 120mm radiator/fan
- ✅ **240mm+** - 240mm or larger radiators
- ✅ **RGB Lighting** - RGB-enabled coolers
- ✅ **Low Noise** - Quiet/silent operation

## How to Use

### Applying Filters:
1. Click the **"🔍 Filter"** button next to any component dropdown
2. Select one or more filter criteria (checkboxes)
3. Click **"Apply"** to filter the parts list
4. The dropdown will now show only parts matching ALL selected filters

### Multiple Filters:
- Filters use **AND logic** - parts must match ALL selected filters
- Example: Select "8GB+ VRAM" + "NVIDIA" + "Ray Tracing" for high-end NVIDIA GPUs

### Clearing Filters:
- In filter dialog: Click **"Clear All"** to deselect all filters
- Click **"Apply"** to show all parts again
- Button text returns to **"🔍 Filter"** when no filters active

### Active Filter Indicator:
- Button shows count: **"🔍 Filter (2)"** = 2 filters active
- Helps track which categories have filters applied

## Technical Implementation

### Filter System Architecture
```python
# pcbuilder/filters.py
- Filter dataclass: name, display_name, filter_func, category
- ComponentFilters class: Manages all filters
- filter_func: Lambda function testing part attributes
```

### Filter Application
```python
# Filters are applied in real-time:
1. User selects filters in dialog
2. active_filters[category] updated with selected filter names
3. Parts list filtered using component_filters.apply_filters()
4. Dropdown refreshed with filtered results
```

### Filter Functions
Each filter uses a lambda function to test part attributes:
```python
Filter("modular", "Fully Modular", 
       lambda p: "fully modular" in p.get("attributes", {}).get("modular", "").lower(), 
       "PSU")
```

### Smart Name Parsing
- RAM capacity extracted from name: "32GB (2x16GB)" → 32
- GPU brand detection: Checks for "RTX", "GTX", "RX", "Radeon"
- Regex patterns for complex attribute extraction

## Benefits for NEA

### Advanced Programming Concepts:
- ✅ **Lambda Functions**: Functional programming for filter logic
- ✅ **Dataclasses**: Clean filter definition structure
- ✅ **Higher-order Functions**: Functions returning functions
- ✅ **Regex**: Pattern matching for attribute extraction
- ✅ **Dynamic UI**: Real-time filter application

### User Experience:
- ✅ **Intuitive Interface**: Checkbox-based filter selection
- ✅ **Visual Feedback**: Active filter count in button
- ✅ **Flexible Search**: Mix and match multiple criteria
- ✅ **Category-Specific**: Filters tailored to each component type

### Data Management:
- ✅ **Efficient Filtering**: In-memory list comprehension
- ✅ **Maintainable Code**: Centralized filter definitions
- ✅ **Extensible Design**: Easy to add new filters

## Example Workflows

### Building a Budget Gaming PC:
1. **CPU**: Filter for "6+ Cores"
2. **Motherboard**: Filter for "Micro-ATX" + "DDR4 Support"
3. **RAM**: Filter for "16GB+" + "3200 MHz+"
4. **GPU**: Filter for "8GB+ VRAM" + "NVIDIA"
5. **PSU**: Filter for "650W+" + "Semi-Modular"

### High-End Workstation:
1. **CPU**: Filter for "12+ Cores" + "Unlocked"
2. **Motherboard**: Filter for "ATX" + "DDR5 Support"
3. **RAM**: Filter for "32GB+" + "DDR5" + "RGB"
4. **GPU**: Filter for "16GB+ VRAM" + "Ray Tracing"
5. **Storage**: Filter for "NVMe" + "PCIe 4.0" + "1TB+"

### Silent Build:
1. **CPU Cooler**: Filter for "Low Noise"
2. **Case**: Filter for "Mesh Front Panel"
3. **PSU**: Filter for "80+ Platinum" (quieter operation)

## Edge Cases Handled
- ✅ Empty filter results (no parts match criteria)
- ✅ Current selection removed by filter (resets to "None")
- ✅ Filters persist when switching tabs
- ✅ Filter state maintained during refresh
- ✅ Multiple filter combinations tested

## Future Enhancements (Ideas)
- Save filter presets
- Price range filters
- Sort by price/performance
- Filter by availability
- Compatibility-aware filters (only show compatible parts)
