# Guided Component Selection Feature

## Overview
The new guided selection system replaces dropdown menus with an intuitive question-based interface that helps users choose PC components without requiring technical knowledge.

## What Changed

### Before
- Users had to pick from dropdown lists of components
- Required understanding of technical specifications
- Difficult for beginners to make informed choices

### After
- Click "✨ Guided" button for any component
- Answer 3 simple questions about your use case
- System automatically filters and shows matching components
- No technical knowledge required!

## How It Works

### For Each Component Type

#### CPU
1. **Primary use?** (Gaming, Video Editing, Office Work, Streaming)
2. **Overclock?** (Yes/No)
3. **Graphics?** (Separate GPU or Integrated)

#### Motherboard
1. **Case size?** (Full size, Compact, Mini)
2. **Built-in WiFi?** (Yes/No)
3. **RAM type?** (DDR5/DDR4/Either)

#### RAM
1. **Usage?** (Gaming only, Gaming+Multitasking, Content Creation, Basic)
2. **Generation?** (DDR5 or DDR4)
3. **RGB lighting?** (Yes/No)

#### GPU
1. **Resolution?** (1080p, 1440p, 4K, Not for gaming)
2. **Brand?** (NVIDIA, AMD, No preference)
3. **Ray tracing?** (Yes/No)

#### PSU
1. **Build type?** (Budget, Mid-range, High-end)
2. **Cable management?** (Very important, Somewhat, Not important)
3. **Efficiency?** (Very efficient, Standard, Basic)

#### Case
1. **Size?** (Full size, Medium, Small)
2. **Glass panel?** (Yes/No)
3. **Priority?** (Airflow, RGB, Both fine)

#### Storage
1. **Primary use?** (OS+programs, Gaming library, Large files, Budget storage)
2. **Speed?** (Fastest, Fast enough, Space over speed)
3. **Capacity?** (500GB-1TB, 1TB-2TB, 2TB+)

#### Cooler
1. **Type?** (Air, Liquid)
2. **CPU power?** (Budget, High-end, Enthusiast)
3. **RGB?** (Yes/No)

## User Interface

### Builder Tab Changes
- **Labels** instead of dropdown menus show selected components
- **"✨ Guided" button** opens the question dialog (primary action)
- **"🔍 Filter" button** opens advanced technical filters (for experts)
- **"Clear" button** removes the selection

### Guided Dialog
- Large, readable text
- Radio buttons for clear choices
- "Show Results" button displays matching components
- "Reset Answers" clears all selections
- Results show in a sortable list with prices

## Technical Implementation

### New Files
- `pcbuilder/guided_selection.py` - Main guided selection system
  - `GuidedSelector` class: Manages questions and filter mappings
  - `GuidedSelectorDialog` class: UI dialog for guided selection

### Modified Files
- `pcbuilder/ui/views/builder_tab.py`
  - Replaced Combobox widgets with Label widgets
  - Added `_open_guided_selector()` method
  - Updated selection display logic
  - Maintained backward compatibility with filters

### Filter Mapping
Each answer maps to technical filters:
- Example: "Gaming only" → `["16gb"]` filter
- Example: "4K Gaming" → `["16gb_vram"]` filter
- Multiple answers can stack filters for precision

## Benefits

### For Beginners
- ✅ No technical jargon required
- ✅ Questions about actual use, not specs
- ✅ Automatic filtering based on needs
- ✅ Clear, simple interface

### For Advanced Users
- ✅ Still have access to technical filters
- ✅ Can override guided selections
- ✅ Direct access to all components
- ✅ Filter dialog unchanged

## Example Workflow

1. User clicks **"✨ Guided"** next to "GPU"
2. Dialog opens: "Let's find the perfect GPU for you!"
3. User answers:
   - Resolution: **1440p** → filters to 12GB+ VRAM
   - Brand: **NVIDIA** → filters to NVIDIA GPUs
   - Ray tracing: **Yes** → filters to RTX series
4. System shows ~15 matching GPUs instead of 200+
5. User picks from curated, relevant list
6. GPU is added to build

## Future Enhancements

Potential additions:
- Save favorite answer profiles
- "Why this question?" tooltips
- Visual previews of components
- Budget-aware filtering in questions
- Compatibility-aware questions (e.g., "Your motherboard supports DDR4")
