"""Build PC tab - main builder interface with role-based access control"""
import tkinter as tk
from tkinter import ttk, messagebox
from ...db import list_parts, save_build
from ...compat import run_full_check
from ...auth import session
from ...templates import get_template_builds, load_template_build, get_template_summary
from ...filters import component_filters
from ...guided_selection import GuidedSelectorDialog
import math


class BuilderTab(ttk.Frame):
    """PC Builder tab for selecting parts and checking compatibility"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Current build selection
        self.selected_parts = {
            "CPU": None,
            "Motherboard": None,
            "RAM": None,
            "GPU": None,
            "PSU": None,
            "Case": None,
            "Storage": None,
            "Cooler": None
        }
        
        # Budget tracking
        self.budget = tk.StringVar(value="0")
        self.budget.trace_add("write", lambda *args: self._update_budget_display())
        
        # Cache all parts
        self.all_parts = []
        self.parts_by_category = {}
        
        # Active filters for each category
        self.active_filters = {category: [] for category in self.selected_parts.keys()}
        
        # Component colors for pie chart
        self.component_colors = {
            "CPU": "#FF6B6B",
            "Motherboard": "#4ECDC4",
            "RAM": "#45B7D1",
            "GPU": "#FFA07A",
            "PSU": "#98D8C8",
            "Case": "#F7DC6F",
            "Storage": "#BB8FCE",
            "Cooler": "#85C1E2"
        }
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the builder interface"""
        # Left panel - Part selection
        left_panel = ttk.Frame(self)
        left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Component selection section (top part of left panel)
        selection_section = ttk.Frame(left_panel)
        selection_section.pack(side="top", fill="both", expand=True)
        
        # Template builds section
        template_frame = ttk.LabelFrame(selection_section, text="📋 Quick Start Templates")
        template_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(template_frame, text="Load a pre-configured build:", font=("Arial", 9)).pack(pady=5)
        
        template_buttons = ttk.Frame(template_frame)
        template_buttons.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(
            template_buttons, 
            text="💰 Budget", 
            command=lambda: self._load_template('budget'),
            width=12
        ).pack(side="left", padx=2)
        
        ttk.Button(
            template_buttons, 
            text="🎮 Mid-Range", 
            command=lambda: self._load_template('mid_range'),
            width=12
        ).pack(side="left", padx=2)
        
        ttk.Button(
            template_buttons, 
            text="🚀 High-End", 
            command=lambda: self._load_template('high_end'),
            width=12
        ).pack(side="left", padx=2)
        
        ttk.Label(selection_section, text="Select Components", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Scrollable frame for part selection
        canvas = tk.Canvas(selection_section, highlightthickness=0)
        scrollbar = ttk.Scrollbar(selection_section, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create dropdowns for each component category
        self.part_combos = {}
        self.filter_buttons = {}
        
        for category in self.selected_parts.keys():
            # Main row with label and buttons
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(frame, text=f"{category}:", width=12, anchor="w").pack(side="left")
            
            # Selected part display (read-only label style)
            part_display = ttk.Label(frame, text="Not selected", 
                                    relief="sunken", anchor="w", 
                                    background="white", foreground="#666")
            part_display.pack(side="left", padx=5, fill="x", expand=True)
            self.part_combos[category] = part_display
            
            # Guided selection button (main action)
            guided_btn = ttk.Button(frame, text="✨ Guided", width=8, 
                                   command=lambda cat=category: self._open_guided_selector(cat),
                                   style="Accent.TButton")
            guided_btn.pack(side="left", padx=2)
            
            # Filter button (advanced)
            filter_btn = ttk.Button(frame, text="🔍 Filter", width=8, 
                                   command=lambda cat=category: self._show_filters(cat))
            filter_btn.pack(side="left", padx=2)
            self.filter_buttons[category] = filter_btn
            
            clear_btn = ttk.Button(frame, text="Clear", width=6, 
                                  command=lambda cat=category: self._clear_part(cat))
            clear_btn.pack(side="left")
        
        # Beginner's Guide Panel (bottom of left panel)
        self._create_guide_panel(left_panel)
        
        # Right panel - Build summary and compatibility
        right_panel = ttk.Frame(self)
        right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(right_panel, text="Build Summary", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Budget input section
        budget_frame = ttk.LabelFrame(right_panel, text="💰 Budget Tracker")
        budget_frame.pack(fill="x", padx=5, pady=5)
        
        budget_input_frame = ttk.Frame(budget_frame)
        budget_input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(budget_input_frame, text="Budget: £", font=("Arial", 10, "bold")).pack(side="left")
        budget_entry = ttk.Entry(budget_input_frame, textvariable=self.budget, width=15, font=("Arial", 10))
        budget_entry.pack(side="left", padx=5)
        
        self.budget_status_label = ttk.Label(budget_input_frame, text="", font=("Arial", 9))
        self.budget_status_label.pack(side="left", padx=10)
        
        # Clear Build button in budget section
        ttk.Button(budget_input_frame, text="🗑️ Clear Build", command=self._clear_all).pack(side="right", padx=5)
        
        # Pie chart canvas
        chart_container = ttk.Frame(budget_frame)
        chart_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.pie_canvas = tk.Canvas(chart_container, width=200, height=200, bg='white', highlightthickness=1, highlightbackground='#ccc')
        self.pie_canvas.pack(side="left", padx=5)
        
        # Legend frame
        self.legend_frame = ttk.Frame(chart_container)
        self.legend_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Build summary text
        summary_frame = ttk.LabelFrame(right_panel, text="Selected Parts")
        summary_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.summary_text = tk.Text(summary_frame, height=12, width=50, wrap="word", state="disabled")
        self.summary_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # PC Statistics Panel
        stats_frame = ttk.LabelFrame(right_panel, text="📊 PC Statistics")
        stats_frame.pack(fill="both", padx=5, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=6, width=50, wrap="word", state="disabled", font=("Arial", 9))
        self.stats_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Compatibility results
        compat_frame = ttk.LabelFrame(right_panel, text="Compatibility Check")
        compat_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.compat_text = tk.Text(compat_frame, height=10, width=50, wrap="word", state="disabled")
        self.compat_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Check Compatibility", command=self._check_compatibility).pack(side="left", padx=5)
        self.save_btn = ttk.Button(button_frame, text="Save Build", command=self._save_build)
        self.save_btn.pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear All", command=self._clear_all).pack(side="left", padx=5)
    
    def _create_guide_panel(self, parent):
        """Create the beginner's guide panel"""
        guide_frame = ttk.LabelFrame(parent, text="📚 Beginner's Guide")
        guide_frame.pack(side="bottom", fill="both", padx=5, pady=5)
        
        # Create notebook for different guide sections
        guide_notebook = ttk.Notebook(guide_frame)
        guide_notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tab 1: Getting Started
        start_frame = ttk.Frame(guide_notebook)
        guide_notebook.add(start_frame, text="Getting Started")
        
        start_text = tk.Text(start_frame, wrap="word", height=8, font=("Arial", 9))
        start_text.pack(fill="both", expand=True, padx=5, pady=5)
        start_text.insert("1.0", """🎯 How to Build Your PC:

1. Start with the CPU - This determines your socket type
2. Choose a compatible Motherboard (matching socket)
3. Select RAM that matches your motherboard type
4. Pick a GPU for gaming/graphics work
5. Choose a PSU with enough wattage
6. Select a Case that fits everything
7. Add Storage for your files
8. Add a Cooler to keep CPU cool

💡 Tip: Click "Check Compatibility" after selecting parts!""")
        start_text.config(state="disabled")
        
        # Tab 2: Component Explanations
        explain_frame = ttk.Frame(guide_notebook)
        guide_notebook.add(explain_frame, text="Components")
        
        explain_scroll = tk.Scrollbar(explain_frame)
        explain_scroll.pack(side="right", fill="y")
        
        explain_text = tk.Text(explain_frame, wrap="word", height=8, font=("Arial", 9), yscrollcommand=explain_scroll.set)
        explain_text.pack(fill="both", expand=True, padx=5, pady=5)
        explain_scroll.config(command=explain_text.yview)
        
        explain_text.insert("1.0", """🔧 Component Guide:

CPU (Processor):
• The "brain" of your PC
• Intel uses LGA1700 sockets (i3, i5, i7)
• AMD uses AM4 or AM5 sockets (Ryzen 5, 7, 9)
• More cores = better multitasking

Motherboard:
• Connects all components together
• Must match CPU socket (LGA1700 or AM4/AM5)
• Size: ATX (large), micro-ATX (medium), mini-ITX (small)
• Check if it supports DDR4 or DDR5 RAM

RAM (Memory):
• Short-term storage for running programs
• 16GB minimum for gaming, 32GB for heavy work
• Must match motherboard type (DDR4 or DDR5)
• Higher MHz = faster performance

GPU (Graphics Card):
• Handles graphics and gaming
• NVIDIA RTX or AMD Radeon
• Check length fits in your case
• Budget: £200-300, Mid: £400-600, High: £600+

PSU (Power Supply):
• Powers all components
• Calculate total wattage + 25% headroom
• 80+ Bronze/Gold/Platinum = efficiency rating
• Don't cheap out on this!

Case:
• Houses all components
• Must fit motherboard size
• Check GPU length clearance
• Good airflow = cooler temps

Storage:
• NVMe SSD = Fastest (for OS and games)
• SATA SSD = Good for storage
• 500GB minimum, 1TB recommended

Cooler:
• Keeps CPU from overheating
• Air coolers = quieter, cheaper
• AIO liquid coolers = better cooling, pricier
• Check socket compatibility""")
        explain_text.config(state="disabled")
        
        # Tab 3: Common Mistakes
        mistakes_frame = ttk.Frame(guide_notebook)
        guide_notebook.add(mistakes_frame, text="Common Mistakes")
        
        mistakes_text = tk.Text(mistakes_frame, wrap="word", height=8, font=("Arial", 9))
        mistakes_text.pack(fill="both", expand=True, padx=5, pady=5)
        mistakes_text.insert("1.0", """⚠️ Avoid These Mistakes:

❌ Mismatched CPU & Motherboard Socket
• Intel i5 (LGA1700) won't fit AM4 motherboard
• Always check socket compatibility!

❌ Wrong RAM Type
• DDR4 RAM won't work in DDR5 motherboard
• Check motherboard specifications

❌ Insufficient PSU Wattage
• High-end GPU + CPU needs 750W+ PSU
• Budget builds need 550W minimum
• Add 25% headroom for safety

❌ GPU Too Large for Case
• Check GPU length (e.g., 285mm)
• Check case max GPU clearance
• Most mid-towers fit up to 350mm

❌ Incompatible Cooler
• LGA1700 coolers don't fit AM4 sockets
• Check cooler socket compatibility

✅ Pro Tips:
• Start with CPU, then motherboard
• Use "Check Compatibility" button often
• Budget 20-30% on GPU for gaming
• Don't forget Windows license (£100+)
• Watch build guides on YouTube!""")
        mistakes_text.config(state="disabled")
        
        # Tab 4: Budget Tips
        budget_frame = ttk.Frame(guide_notebook)
        guide_notebook.add(budget_frame, text="Budget Tips")
        
        budget_text = tk.Text(budget_frame, wrap="word", height=8, font=("Arial", 9))
        budget_text.pack(fill="both", expand=True, padx=5, pady=5)
        budget_text.insert("1.0", """💰 Budget Building Tips:

Entry Level (£500-700):
• CPU: Intel i3 or Ryzen 5 5600
• GPU: RX 6600 or RTX 4060
• RAM: 16GB DDR4
• Storage: 500GB NVMe SSD
• PSU: 550W Bronze

Mid-Range (£800-1200):
• CPU: Intel i5 or Ryzen 5 5600X
• GPU: RX 7600 or RTX 4060 Ti
• RAM: 16-32GB DDR4
• Storage: 1TB NVMe SSD
• PSU: 650W Gold

High-End (£1500+):
• CPU: Intel i7 or Ryzen 7 7800X3D
• GPU: RTX 4070/4080 or RX 7800 XT
• RAM: 32GB DDR5
• Storage: 1-2TB NVMe SSD
• PSU: 850W+ Gold

💡 Money-Saving Tips:
• Buy CPU without 'K' (no overclocking)
• Use stock cooler if included
• Prioritize GPU for gaming
• 16GB RAM is fine for most users
• Get case on sale (£50-100)
• Re-use old Windows license if possible

🛒 Where to Buy (UK):
• Overclockers UK - Great service
• Scan Computers - Good prices
• Amazon UK - Fast delivery
• CCL Online - Bundle deals""")
        budget_text.config(state="disabled")
    
    def _open_guided_selector(self, category: str):
        """Open the guided selector dialog for a component category"""
        def on_part_selected(part):
            """Callback when a part is selected from guided dialog"""
            self.selected_parts[category] = part
            # Update the display label
            part_display = self.part_combos[category]
            part_display.config(text=part["name"], foreground="black")
            self._update_summary()
        
        # Open the guided selector dialog
        GuidedSelectorDialog(self, category, on_part_selected)
    
    def _on_part_selected(self, category):
        """Handle part selection from dropdown"""
        combo = self.part_combos[category]
        selection = combo.get()
        
        if not selection or selection == "(None)":
            self.selected_parts[category] = None
        else:
            # Find the part from cached list
            parts = self.parts_by_category.get(category, [])
            for part in parts:
                if part["name"] == selection:
                    self.selected_parts[category] = part
                    break
        
        self._update_summary()
    
    def _clear_part(self, category):
        """Clear a selected part"""
        self.selected_parts[category] = None
        # Update the display label
        part_display = self.part_combos[category]
        part_display.config(text="Not selected", foreground="#666")
        self._update_summary()
    
    def _load_template(self, template_id: str):
        """Load a template build"""
        # Get template summary
        summary = get_template_summary(template_id)
        if not summary:
            messagebox.showerror("Error", "Template not found")
            return
        
        # Confirm with user
        message = (
            f"{summary['name']}\n\n"
            f"{summary['description']}\n\n"
            f"Target Price: {summary['target_price']}\n"
            f"Actual Price: £{summary['actual_price']:.2f}\n\n"
            f"This will replace your current build. Continue?"
        )
        
        if not messagebox.askyesno("Load Template Build", message):
            return
        
        # Load template parts
        template_parts = load_template_build(template_id)
        if not template_parts:
            messagebox.showerror("Error", "Failed to load template")
            return
        
        # Update selected parts and UI
        missing_parts = []
        for category, part in template_parts.items():
            if part:
                self.selected_parts[category] = part
                part_display = self.part_combos[category]
                part_display.config(text=part['name'], foreground="black")
            else:
                self.selected_parts[category] = None
                part_display = self.part_combos[category]
                part_display.config(text="Not selected", foreground="#666")
                missing_parts.append(category)
        
        # Update displays
        self._update_summary()
        
        # Show warning if parts are missing
        if missing_parts:
            messagebox.showwarning(
                "Template Loaded with Warnings",
                f"Template loaded successfully!\n\n"
                f"Note: The following components were not found in the database:\n"
                f"{', '.join(missing_parts)}\n\n"
                f"You may need to select alternative parts."
            )
        else:
            messagebox.showinfo(
                "Template Loaded",
                f"{summary['name']} loaded successfully!\n\n"
                f"Total: £{summary['actual_price']:.2f}"
            )
    
    def _show_filters(self, category: str):
        """Show filter dialog for a category"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Filter {category}")
        dialog.geometry("350x500")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Filters for {category}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Get available filters for this category
        available_filters = component_filters.get_filters_for_category(category)
        
        if not available_filters:
            ttk.Label(dialog, text="No filters available for this component").pack(pady=20)
            ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
            return
        
        # Scrollable frame for filters
        canvas = tk.Canvas(dialog, highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        filter_frame = ttk.Frame(canvas)
        
        filter_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=filter_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Create checkboxes for each filter
        filter_vars = {}
        for filter_obj in available_filters:
            var = tk.BooleanVar(value=filter_obj.name in self.active_filters[category])
            filter_vars[filter_obj.name] = var
            
            cb = ttk.Checkbutton(filter_frame, text=filter_obj.display_name, 
                               variable=var)
            cb.pack(anchor="w", pady=3, padx=10)
        
        # Button frame
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def apply_filters():
            # Update active filters
            self.active_filters[category] = [
                fname for fname, var in filter_vars.items() if var.get()
            ]
            
            # Update filter button text to show active count
            active_count = len(self.active_filters[category])
            if active_count > 0:
                self.filter_buttons[category].config(text=f"🔍 Filter ({active_count})")
            else:
                self.filter_buttons[category].config(text="🔍 Filter")
            
            # Refresh the parts list for this category
            self._refresh_category_parts(category)
            
            dialog.destroy()
        
        def clear_filters():
            for var in filter_vars.values():
                var.set(False)
        
        ttk.Button(btn_frame, text="Apply", command=apply_filters).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear All", command=clear_filters).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="right", padx=5)
    
    def _refresh_category_parts(self, category: str):
        """Refresh the parts list for a specific category with filters applied"""
        # Get all parts for this category
        all_category_parts = self.parts_by_category.get(category, [])
        
        # Apply filters
        filtered_parts = component_filters.apply_filters(
            all_category_parts, 
            category, 
            self.active_filters[category]
        )
        
        # Check if current selection is still valid
        current_part = self.selected_parts[category]
        if current_part and current_part not in filtered_parts:
            # Clear selection if it doesn't match filters
            self.selected_parts[category] = None
            part_display = self.part_combos[category]
            part_display.config(text="Not selected", foreground="#666")
            self._update_summary()
    
    def _clear_all(self):
        """Clear all selected parts"""
        for category in self.selected_parts.keys():
            self._clear_part(category)
    
    def _update_summary(self):
        """Update the build summary text"""
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        
        total_price = 0.0
        for category, part in self.selected_parts.items():
            if part:
                price = part.get("price", 0)
                total_price += price
                self.summary_text.insert(tk.END, f"{category}: {part['name']} (£{price:.2f})\n")
            else:
                self.summary_text.insert(tk.END, f"{category}: (Not selected)\n")
        
        self.summary_text.insert(tk.END, f"\nTotal Price: £{total_price:.2f}")
        self.summary_text.config(state="disabled")
        
        # Update statistics panel
        self._update_stats()
        
        # Update budget display and pie chart
        self._update_budget_display()
    
    def _update_stats(self):
        """Update the PC statistics panel with key specs"""
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        
        stats = []
        
        # CPU Info
        cpu = self.selected_parts.get("CPU")
        if cpu:
            attrs = cpu.get("attributes", {})
            cores = attrs.get("cores", "?")
            threads = attrs.get("threads", "?")
            stats.append(f"🖥️ CPU: {cores} cores / {threads} threads")
        
        # RAM Info
        ram = self.selected_parts.get("RAM")
        if ram:
            attrs = ram.get("attributes", {})
            name = ram.get("name", "")
            
            # Try to extract total capacity from name (e.g., "32GB (2x16GB)" or "16GB (2x8GB)")
            import re
            # Look for pattern like "32GB" or "16GB" at the start
            capacity_match = re.search(r'(\d+)GB', name)
            if capacity_match:
                total_capacity = capacity_match.group(1)
                # Look for stick configuration like "(2x8GB)" or "(2x16GB)"
                config_match = re.search(r'\((\d+x\d+)GB\)', name)
                if config_match:
                    stats.append(f"💾 RAM: {total_capacity}GB ({config_match.group(1)}GB)")
                else:
                    stats.append(f"💾 RAM: {total_capacity}GB")
            else:
                # Fallback to sticks count if no capacity found
                sticks = attrs.get("sticks", "?")
                stats.append(f"💾 RAM: {sticks} sticks")
        
        # GPU Info
        gpu = self.selected_parts.get("GPU")
        if gpu:
            attrs = gpu.get("attributes", {})
            memory = attrs.get("memory", "?")
            # Memory might already include "GB", so don't add it again
            if "GB" in str(memory):
                stats.append(f"🎮 GPU Memory: {memory} VRAM")
            else:
                stats.append(f"🎮 GPU Memory: {memory}GB VRAM")
        
        # Storage Info
        storage = self.selected_parts.get("Storage")
        if storage:
            attrs = storage.get("attributes", {})
            capacity = attrs.get("capacity", "?")
            interface = attrs.get("interface", "?")
            stats.append(f"💿 Storage: {capacity}GB {interface}")
        
        # PSU Info
        psu = self.selected_parts.get("PSU")
        if psu:
            attrs = psu.get("attributes", {})
            wattage = attrs.get("wattage", "?")
            efficiency = attrs.get("efficiency", "")
            if efficiency:
                stats.append(f"⚡ PSU: {wattage}W ({efficiency})")
            else:
                stats.append(f"⚡ PSU: {wattage}W")
        
        # Total Power Draw (estimated)
        total_power = 0
        cpu_power = 0
        gpu_power = 0
        
        if cpu:
            try:
                cpu_power = int(cpu.get("attributes", {}).get("power_draw", 0))
            except (ValueError, TypeError):
                cpu_power = 0
        
        if gpu:
            try:
                gpu_power = int(gpu.get("attributes", {}).get("power_draw", 0))
            except (ValueError, TypeError):
                gpu_power = 0
        
        if cpu_power > 0 or gpu_power > 0:
            # Add CPU + GPU + ~100W for other components
            total_power = cpu_power + gpu_power + 100
            stats.append(f"📊 Est. Power Draw: ~{total_power}W")
        
        # Case Info
        case = self.selected_parts.get("Case")
        if case:
            attrs = case.get("attributes", {})
            form_factor = attrs.get("form_factor", "")
            if form_factor:
                stats.append(f"📦 Case: {form_factor}")
        
        # Display stats
        if stats:
            self.stats_text.insert(tk.END, "\n".join(stats))
        else:
            self.stats_text.insert(tk.END, "No components selected yet")
        
        self.stats_text.config(state="disabled")
    
    def _check_compatibility(self):
        """Run compatibility check and display results"""
        results = run_full_check(self.selected_parts)
        
        self.compat_text.config(state="normal")
        self.compat_text.delete("1.0", tk.END)
        
        all_ok = True
        for rule_id, passed, message in results:
            status = "✓ OK" if passed else "✗ FAIL"
            color = "green" if passed else "red"
            
            start_pos = self.compat_text.index(tk.END)
            self.compat_text.insert(tk.END, f"{status}: {message}\n")
            end_pos = self.compat_text.index(tk.END)
            
            # Color the status
            self.compat_text.tag_add(rule_id, start_pos, end_pos)
            self.compat_text.tag_config(rule_id, foreground=color)
            
            if not passed:
                all_ok = False
        
        if all_ok:
            self.compat_text.insert(tk.END, "\n✓ All compatibility checks passed!")
        else:
            self.compat_text.insert(tk.END, "\n⚠ Some compatibility issues detected")
        
        self.compat_text.config(state="disabled")
    
    def _save_build(self):
        """Save the current build (requires STANDARD role or higher)"""
        # Check permissions
        current_user = session.get_current_user()
        if not current_user or not current_user.can_save():
            messagebox.showwarning(
                "Permission Denied",
                "You must be signed in to save builds.\n\n"
                "Guest users can build and check compatibility,\n"
                "but cannot save builds.\n\n"
                "Please create an account or sign in to save your build."
            )
            return
        
        if not any(self.selected_parts.values()):
            messagebox.showwarning("No Parts", "Please select at least one part before saving")
            return
        
        # Prompt for build name
        dialog = tk.Toplevel(self)
        dialog.title("Save Build")
        dialog.geometry("300x120")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Build Name:").pack(pady=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def do_save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid Name", "Please enter a build name")
                return
            
            try:
                build_id, share_key = save_build(self.controller.current_user_id, name, self.selected_parts)
                dialog.destroy()
                
                # Show success with share key
                share_dialog = tk.Toplevel(self)
                share_dialog.title("Build Saved!")
                share_dialog.geometry("400x200")
                share_dialog.transient(self)
                share_dialog.grab_set()
                
                ttk.Label(share_dialog, text=f"✓ Build '{name}' saved successfully!", 
                         font=("Arial", 11, "bold"), foreground="green").pack(pady=15)
                
                ttk.Label(share_dialog, text="Share this key with others to share your build:", 
                         font=("Arial", 9)).pack(pady=5)
                
                # Share key display with copy button
                key_frame = ttk.Frame(share_dialog)
                key_frame.pack(pady=10)
                
                key_entry = ttk.Entry(key_frame, width=12, font=("Courier", 14, "bold"), 
                                     justify="center", state="readonly")
                key_entry.pack(side="left", padx=5)
                key_entry.configure(state="normal")
                key_entry.insert(0, share_key)
                key_entry.configure(state="readonly")
                
                def copy_key():
                    share_dialog.clipboard_clear()
                    share_dialog.clipboard_append(share_key)
                    copy_btn.config(text="✓ Copied!")
                    share_dialog.after(2000, lambda: copy_btn.config(text="📋 Copy"))
                
                copy_btn = ttk.Button(key_frame, text="📋 Copy", command=copy_key)
                copy_btn.pack(side="left", padx=5)
                
                ttk.Button(share_dialog, text="OK", command=share_dialog.destroy).pack(pady=15)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save build: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=do_save).pack(pady=10)
    
    def _update_budget_display(self):
        """Update budget status and draw pie chart"""
        try:
            budget_value = float(self.budget.get() or 0)
        except ValueError:
            budget_value = 0
        
        # Calculate total cost
        total_cost = sum(part.get("price", 0) for part in self.selected_parts.values() if part)
        
        # Update status label
        if budget_value > 0:
            remaining = budget_value - total_cost
            if remaining >= 0:
                self.budget_status_label.config(
                    text=f"Remaining: £{remaining:.2f}",
                    foreground="green"
                )
            else:
                self.budget_status_label.config(
                    text=f"Over budget: £{abs(remaining):.2f}",
                    foreground="red"
                )
        else:
            self.budget_status_label.config(text="", foreground="black")
        
        # Draw pie chart
        self._draw_pie_chart()
    
    def _draw_pie_chart(self):
        """Draw pie chart showing budget allocation by component"""
        self.pie_canvas.delete("all")
        
        # Clear legend
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        
        # Calculate component costs
        component_costs = {}
        total_cost = 0
        
        for category, part in self.selected_parts.items():
            if part:
                price = part.get("price", 0)
                component_costs[category] = price
                total_cost += price
        
        # Get budget value
        try:
            budget_value = float(self.budget.get() or 0)
        except ValueError:
            budget_value = 0
        
        # Draw pie chart
        center_x = center_y = 100
        radius = 80
        start_angle = 0
        
        # If no budget is set, just show component allocation
        if budget_value == 0:
            if total_cost == 0:
                # No parts selected and no budget - show message
                self.pie_canvas.create_text(
                    100, 100,
                    text="Set a budget\nand add components",
                    font=("Arial", 10),
                    fill="#666",
                    justify="center"
                )
                return
            
            # Show components without budget comparison
            total_for_calc = total_cost
        else:
            # Use budget as the total for percentage calculations
            total_for_calc = budget_value
        
        # Sort by price (highest first) for better visualization
        sorted_components = sorted(component_costs.items(), key=lambda x: x[1], reverse=True)
        
        # Draw component slices
        for category, price in sorted_components:
            if price > 0:
                # Calculate slice angle based on budget or total cost
                percentage = (price / total_for_calc) * 100
                extent = (price / total_for_calc) * 360
                
                # Draw pie slice
                color = self.component_colors.get(category, "#CCCCCC")
                self.pie_canvas.create_arc(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    start=start_angle, extent=extent,
                    fill=color, outline="white", width=2
                )
                
                # Add legend entry
                legend_row = ttk.Frame(self.legend_frame)
                legend_row.pack(fill="x", pady=2)
                
                # Color box
                color_canvas = tk.Canvas(legend_row, width=16, height=16, 
                                        bg=color, highlightthickness=1, 
                                        highlightbackground="#999")
                color_canvas.pack(side="left", padx=(0, 5))
                
                # Label with percentage and price
                label_text = f"{category}: {percentage:.1f}% (£{price:.2f})"
                ttk.Label(legend_row, text=label_text, font=("Arial", 8)).pack(side="left")
                
                start_angle += extent
        
        # Draw remaining budget as grey slice (if budget is set and there's remaining)
        if budget_value > 0 and total_cost < budget_value:
            remaining_budget = budget_value - total_cost
            remaining_percentage = (remaining_budget / total_for_calc) * 100
            remaining_extent = (remaining_budget / total_for_calc) * 360
            
            # Draw grey slice for remaining budget
            self.pie_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=remaining_extent,
                fill="#D3D3D3", outline="white", width=2
            )
            
            # Add legend entry for remaining budget
            legend_row = ttk.Frame(self.legend_frame)
            legend_row.pack(fill="x", pady=2)
            
            # Grey color box
            color_canvas = tk.Canvas(legend_row, width=16, height=16, 
                                    bg="#D3D3D3", highlightthickness=1, 
                                    highlightbackground="#999")
            color_canvas.pack(side="left", padx=(0, 5))
            
            # Label
            label_text = f"Remaining: {remaining_percentage:.1f}% (£{remaining_budget:.2f})"
            ttk.Label(legend_row, text=label_text, font=("Arial", 8)).pack(side="left")
        
        # Draw center circle for donut effect
        inner_radius = 35
        self.pie_canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            fill="white", outline="white"
        )
        
        # Add text in center
        if budget_value > 0:
            # Show used vs budget
            self.pie_canvas.create_text(
                center_x, center_y - 8,
                text=f"£{total_cost:.0f}",
                font=("Arial", 11, "bold"),
                fill="#333"
            )
            self.pie_canvas.create_text(
                center_x, center_y + 8,
                text=f"of £{budget_value:.0f}",
                font=("Arial", 8),
                fill="#666"
            )
        else:
            # Just show total
            self.pie_canvas.create_text(
                center_x, center_y,
                text=f"£{total_cost:.0f}",
                font=("Arial", 11, "bold"),
                fill="#333"
            )
    
    def refresh(self):
        """Refresh the parts list and update UI based on user permissions"""
        self.all_parts = list_parts()
        self.parts_by_category = {}
        
        for part in self.all_parts:
            category = part["category"]
            if category not in self.parts_by_category:
                self.parts_by_category[category] = []
            self.parts_by_category[category].append(part)
        
        # Update save button based on user permissions
        current_user = session.get_current_user()
        if current_user and current_user.can_save():
            self.save_btn.config(state="normal")
        else:
            self.save_btn.config(state="disabled")
            if current_user and current_user.is_guest():
                # Add tooltip or update button text
                self.save_btn.config(text="Save Build (Sign in required)")
        
        self._update_summary()
