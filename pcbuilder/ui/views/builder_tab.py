"""Build PC tab - main builder interface with role-based access control"""
import tkinter as tk
from tkinter import ttk, messagebox
from ...database_manager import get_database_manager
from ...compat import run_full_check
from ...auth import session
from ...templates import get_template_builds, load_template_build, get_template_summary
from ...guided_selection import GuidedSelectorDialog
from ...undo_redo import UndoRedoManager
import math


def list_parts():
    """Get all components as dictionaries"""
    db = get_database_manager()
    components = db.get_all_components()
    return [comp.to_dict() for comp in components]


def save_build(user_id: int, build_name: str, parts: dict):
    """Save a build to the database"""
    from ...models import Build, ComponentFactory
    db = get_database_manager()
    
    build = Build(build_id=None, name=build_name, user_id=user_id)
    for category, part_data in parts.items():
        if part_data:
            component = ComponentFactory.create_component(
                part_data['id'], part_data['name'], part_data['category'],
                part_data['price'], part_data.get('attributes', {})
            )
            build.add_component(component)
    
    return db.save_build(build)


class RoundedButton(tk.Canvas):
    """Custom button with rounded corners"""
    def __init__(self, parent, text="", command=None, bg="#2196F3", fg="white", 
                 width=120, height=40, radius=8, font=("Segoe UI", 10, "bold"), **kwargs):
        # Get parent background color
        try:
            parent_bg = parent.cget('background')
        except:
            parent_bg = "#e8f4f8"
        
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, background=parent_bg, **kwargs)
        
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.hover_color = self._darken_color(bg, 0.9)
        self.text = text
        self.radius = radius
        self.font = font
        
        self._draw_button()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _darken_color(self, color, factor):
        """Darken a hex color by a factor"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _draw_button(self, color=None):
        """Draw rounded rectangle button"""
        if color is None:
            color = self.bg_color
        
        self.delete("all")
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        r = self.radius
        
        # Draw rounded rectangle
        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=color, outline="")
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=color, outline="")
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=color, outline="")
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=color, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=color, outline="")
        self.create_rectangle(0, r, w, h-r, fill=color, outline="")
        
        # Draw text
        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, font=self.font)
    
    def _on_click(self, event):
        """Handle button click"""
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        """Handle mouse enter"""
        self._draw_button(self.hover_color)
        self.configure(cursor="hand2")
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        self._draw_button()
        self.configure(cursor="")


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
        
        # Undo/Redo manager using STACK data structure
        self.undo_redo_manager = UndoRedoManager(max_history=20)
        
        # Budget tracking
        self.budget = tk.StringVar(value="0")
        self.budget.trace_add("write", lambda *args: self._update_budget_display())
        
        # Cache all parts
        self.all_parts = []
        self.parts_by_category = {}
        
        # Template selection
        self.selected_template = None
        
        # Initialize part lists from database
        self.parts_by_category = {}
        
        # Component colors for pie chart - More vibrant
        self.component_colors = {
            "CPU": "#FF6B6B",      # Coral red
            "Motherboard": "#4ECDC4",  # Turquoise
            "RAM": "#45B7D1",      # Sky blue
            "GPU": "#FFA07A",      # Light salmon
            "PSU": "#98D8C8",      # Mint
            "Case": "#FFD93D",     # Bright yellow
            "Storage": "#BB8FCE",  # Lavender
            "Cooler": "#85C1E2"    # Light blue
        }
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the builder interface with modern styling"""
        # Main container with better proportions
        main_container = ttk.PanedWindow(self, orient="horizontal")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Part selection (60% width)
        left_panel = ttk.Frame(main_container, style="TFrame")
        main_container.add(left_panel, weight=60)
        
        # Right panel - Build summary and compatibility (40% width)
        right_panel = ttk.Frame(main_container, style="TFrame")
        main_container.add(right_panel, weight=40)
        
        # Component selection section (top part of left panel)
        selection_section = ttk.Frame(left_panel, style="TFrame")
        selection_section.pack(side="top", fill="both", expand=True)
        
        # Header with modern styling
        header_frame = ttk.Frame(selection_section, style="TFrame")
        header_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ttk.Label(header_frame, text="Build Your PC", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Select components to create your perfect build", 
                 style="Secondary.TLabel").pack(anchor="w", pady=(2, 0))
        
        # Template builds section - Modern card style with color
        template_frame = ttk.LabelFrame(selection_section, text="🚀 Quick Start Templates", 
                                       padding=15, style="Primary.TLabelframe")
        template_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        ttk.Label(template_frame, text="Start with a pre-configured build:", 
                 font=("Segoe UI", 9), style="Secondary.TLabel").pack(pady=(0, 8))
        
        template_buttons = ttk.Frame(template_frame, style="TFrame")
        template_buttons.pack(fill="x", pady=(0, 5))
        
        # Use rounded buttons for templates - Increased width for text
        budget_btn = RoundedButton(template_buttons, text="💰 Budget Build", 
                                  command=lambda: self._load_template('budget'),
                                  bg="#4CAF50", width=160, height=48, radius=10)
        budget_btn.pack(side="left", padx=5, expand=True)
        
        gaming_btn = RoundedButton(template_buttons, text="🎮 Gaming Build", 
                                  command=lambda: self._load_template('mid_range'),
                                  bg="#2196F3", width=160, height=48, radius=10)
        gaming_btn.pack(side="left", padx=5, expand=True)
        
        highend_btn = RoundedButton(template_buttons, text="🚀 High-End Build", 
                                   command=lambda: self._load_template('high_end'),
                                   bg="#9C27B0", width=160, height=48, radius=10)
        highend_btn.pack(side="left", padx=5, expand=True)
        
        # Component selection header
        component_header = ttk.Frame(selection_section, style="TFrame")
        component_header.pack(fill="x", padx=10, pady=(5, 10))
        
        ttk.Label(component_header, text="Components", style="Subtitle.TLabel").pack(side="left")
        ttk.Label(component_header, text="Select each component for your build", 
                 style="Secondary.TLabel", font=("Segoe UI", 9)).pack(side="left", padx=(10, 0))
        
        # Scrollable frame for part selection
        canvas = tk.Canvas(selection_section, highlightthickness=0, bg="#f0f2f5")
        scrollbar = ttk.Scrollbar(selection_section, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create dropdowns for each component category with modern styling
        self.part_combos = {}
        
        # Component labels
        component_icons = {
            "CPU": "",
            "Motherboard": "",
            "RAM": "",
            "GPU": "",
            "PSU": "",
            "Case": "",
            "Storage": "💿",
            "Cooler": "❄️"
        }
        
        # Icon background colors for visual variety
        icon_bg_colors = {
            "CPU": "#FFE5E5",      # Light red
            "Motherboard": "#E0F7FA",  # Light cyan
            "RAM": "#E3F2FD",      # Light blue
            "GPU": "#FFF3E0",      # Light orange
            "PSU": "#E8F5E9",      # Light green
            "Case": "#FFF9C4",     # Light yellow
            "Storage": "#F3E5F5",  # Light purple
            "Cooler": "#E1F5FE"    # Light blue
        }
        
        for category in self.selected_parts.keys():
            # Card-style container for each component with colored background
            card_frame = ttk.Frame(scrollable_frame, style="TFrame")
            card_frame.pack(fill="x", padx=10, pady=6)
            
            # Component row with modern layout and colored left border
            row_frame = tk.Frame(card_frame, bg="white", relief="solid", borderwidth=1, 
                               highlightbackground=self.component_colors[category], 
                               highlightthickness=3, highlightcolor=self.component_colors[category])
            row_frame.pack(fill="x", padx=2, pady=2)
            
            # Icon with colored background
            icon = component_icons.get(category, "🔧")
            icon_bg = icon_bg_colors.get(category, "#f0f0f0")
            label_frame = tk.Frame(row_frame, bg=icon_bg)
            label_frame.pack(side="left", padx=0, pady=0, ipadx=10, ipady=8)
            
            tk.Label(label_frame, text=icon, font=("Segoe UI", 16), bg=icon_bg).pack(side="left", padx=(8, 8))
            tk.Label(label_frame, text=category, font=("Segoe UI", 10, "bold"), bg=icon_bg).pack(side="left", padx=(0, 8))
            
            # Selected part display (modern card style)
            part_display_frame = tk.Frame(row_frame, bg="white")
            part_display_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            part_display = tk.Label(part_display_frame, text="Not selected", 
                                   relief="flat", anchor="w", 
                                   background="#f8f9fa", foreground="#6c757d",
                                   font=("Segoe UI", 9), padx=10, pady=6)
            part_display.pack(fill="x")
            self.part_combos[category] = part_display
            
            # Action buttons (modern compact)
            button_frame = tk.Frame(row_frame, bg="white")
            button_frame.pack(side="right", padx=10, pady=8)
            
            # Guided selection button (primary action) - rounded with better width
            guided_btn = RoundedButton(button_frame, text="Guide", 
                                      command=lambda cat=category: self._open_guided_selector(cat),
                                      bg="#2196F3", width=100, height=38, radius=8,
                                      font=("Segoe UI", 9, "bold"))
            guided_btn.pack(side="left", padx=3)
            
            # Clear button (red/danger style) - rounded
            clear_btn = RoundedButton(button_frame, text="✕", 
                                     command=lambda cat=category: self._clear_part(cat),
                                     bg="#F44336", width=38, height=38, radius=8,
                                     font=("Segoe UI", 11, "bold"))
            clear_btn.pack(side="left", padx=3)
        
        # RIGHT PANEL - Build summary and compatibility with modern styling
        # Header
        header_frame = ttk.Frame(right_panel, style="TFrame")
        header_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ttk.Label(header_frame, text="Your Build", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Review your selected components", 
                 style="Secondary.TLabel").pack(anchor="w", pady=(2, 0))
        
        # Budget input section - Modern card with color
        budget_frame = ttk.LabelFrame(right_panel, text="💰 Budget Tracker", 
                                     padding=15, style="Success.TLabelframe")
        budget_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        budget_input_frame = ttk.Frame(budget_frame, style="TFrame")
        budget_input_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(budget_input_frame, text="Budget: £", 
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        budget_entry = ttk.Entry(budget_input_frame, textvariable=self.budget, 
                                width=12, font=("Segoe UI", 11))
        budget_entry.pack(side="left", padx=8)
        
        self.budget_status_label = ttk.Label(budget_input_frame, text="", 
                                            font=("Segoe UI", 10))
        self.budget_status_label.pack(side="left", padx=15)
        
        # Undo button - Using STACK data structure
        self.undo_btn = RoundedButton(budget_input_frame, text="↶ Undo", 
                                     command=self._undo,
                                     bg="#9E9E9E", width=90, height=40, radius=8,
                                     font=("Segoe UI", 9, "bold"))
        self.undo_btn.pack(side="right", padx=3)
        
        # Clear Build button - rounded with better width
        clear_all_btn = RoundedButton(budget_input_frame, text="🗑️ Clear All", 
                                     command=self._clear_all,
                                     bg="#F44336", width=120, height=40, radius=8,
                                     font=("Segoe UI", 9, "bold"))
        clear_all_btn.pack(side="right", padx=5)
        
        # Pie chart canvas - Made more compact
        chart_container = ttk.Frame(budget_frame, style="TFrame")
        chart_container.pack(fill="both", padx=5, pady=(0, 5))
        
        self.pie_canvas = tk.Canvas(chart_container, width=180, height=180, 
                                    bg='white', highlightthickness=0)
        self.pie_canvas.pack(side="left", padx=5)
        
        # Legend frame
        self.legend_frame = ttk.Frame(chart_container, style="TFrame")
        self.legend_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Build summary text - Modern card style (SMALLER)
        summary_frame = ttk.LabelFrame(right_panel, text="📝 Selected Parts", padding=10)
        summary_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Add scrollbar to summary
        summary_scroll_frame = ttk.Frame(summary_frame, style="TFrame")
        summary_scroll_frame.pack(fill="both", expand=True)
        
        summary_scrollbar = ttk.Scrollbar(summary_scroll_frame)
        summary_scrollbar.pack(side="right", fill="y")
        
        self.summary_text = tk.Text(summary_scroll_frame, height=5, width=50, wrap="word", 
                                   state="disabled", yscrollcommand=summary_scrollbar.set,
                                   font=("Segoe UI", 9), bg="white", relief="flat",
                                   borderwidth=0, padx=10, pady=5)
        self.summary_text.pack(side="left", fill="both", expand=True)
        summary_scrollbar.config(command=self.summary_text.yview)
        
        # Compatibility results - LARGER SPACE FOR BETTER VISIBILITY with colorful styling
        compat_frame = ttk.LabelFrame(right_panel, text="Compatibility Check", 
                                     padding=10, style="Primary.TLabelframe")
        compat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Action buttons AT THE TOP of compatibility frame - Rounded buttons with better sizing
        button_frame = tk.Frame(compat_frame, bg="white")
        button_frame.pack(fill="x", pady=(0, 10))
        
        check_btn = RoundedButton(button_frame, text="Check Compatibility", 
                                 command=self._check_compatibility,
                                 bg="#2196F3", width=200, height=45, radius=10,
                                 font=("Segoe UI", 10, "bold"))
        check_btn.pack(side="left", padx=5)
        
        self.save_btn_canvas = RoundedButton(button_frame, text="Save Build", 
                                            command=self._save_build,
                                            bg="#4CAF50", width=150, height=45, radius=10,
                                            font=("Segoe UI", 10, "bold"))
        self.save_btn_canvas.pack(side="left", padx=5)
        self.save_btn = self.save_btn_canvas  # Keep reference for enable/disable
        
        # Add scrollbar for compatibility text
        compat_scroll_frame = ttk.Frame(compat_frame, style="TFrame")
        compat_scroll_frame.pack(fill="both", expand=True)
        
        compat_scrollbar = ttk.Scrollbar(compat_scroll_frame)
        compat_scrollbar.pack(side="right", fill="y")
        
        self.compat_text = tk.Text(compat_scroll_frame, height=30, width=50, wrap="word", 
                                   state="disabled", font=("Segoe UI", 10),
                                   yscrollcommand=compat_scrollbar.set,
                                   bg="white", relief="flat", borderwidth=0,
                                   padx=10, pady=5)
        self.compat_text.pack(side="left", fill="both", expand=True)
        compat_scrollbar.config(command=self.compat_text.yview)
        
        # Initialize undo/redo button states
        self._update_undo_redo_buttons()
    
    def _open_guided_selector(self, category: str):
        """Open the guided selector dialog for a component category"""
        def on_part_selected(part):
            """Callback when a part is selected from guided dialog"""
            # Save state to undo stack before making change
            self._save_current_state()
            
            self.selected_parts[category] = part
            # Update the display label with modern styling
            part_display = self.part_combos[category]
            part_display.config(text=part["name"], foreground="#1c1e21", 
                              background="white", font=("Segoe UI", 9, "bold"))
            self._update_summary()
        
        # Open the guided selector dialog
        GuidedSelectorDialog(self, category, on_part_selected)
    
    def _save_current_state(self):
        """Save current selected parts to undo stack (PUSH operation)"""
        self.undo_redo_manager.save_state(self.selected_parts)
        self._update_undo_redo_buttons()
    
    def _undo(self):
        """Undo last change using STACK data structure (POP from undo_stack)"""
        previous_state = self.undo_redo_manager.undo()
        if previous_state is not None:
            self.selected_parts = previous_state.copy()
            self._update_all_displays()
            self._update_undo_redo_buttons()
    
    def _update_undo_redo_buttons(self):
        """Enable/disable undo button based on stack state"""
        # Enable undo button if undo stack has items
        if self.undo_redo_manager.can_undo():
            self.undo_btn.config(state="normal")
        else:
            self.undo_btn.config(state="disabled")
    
    def _update_all_displays(self):
        """Update all part display labels after undo/redo"""
        for category in self.selected_parts:
            part_display = self.part_combos[category]
            part = self.selected_parts[category]
            if part:
                part_display.config(text=part["name"], foreground="#1c1e21",
                                  background="white", font=("Segoe UI", 9, "bold"))
            else:
                part_display.config(text="(None)", foreground="#757575",
                                  background="#f5f5f5", font=("Segoe UI", 9))
        self._update_summary()
    
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
        # Save state to undo stack before clearing (PUSH operation)
        self._save_current_state()
        
        self.selected_parts[category] = None
        # Update the display label with default styling
        part_display = self.part_combos[category]
        part_display.config(text="Not selected", foreground="#6c757d", 
                          background="#f8f9fa", font=("Segoe UI", 9))
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
        
        # Save state to undo stack before loading template (PUSH operation)
        self._save_current_state()
        
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
        
        self._update_summary()
    
    def _clear_all(self):
        """Clear all selected parts"""
        # Save state to undo stack before clearing all (PUSH operation)
        self._save_current_state()
        
        # Clear all parts without saving individual states
        for category in self.selected_parts.keys():
            self.selected_parts[category] = None
            part_display = self.part_combos[category]
            part_display.config(text="Not selected", foreground="#6c757d",
                              background="#f8f9fa", font=("Segoe UI", 9))
        
        self._update_summary()
    
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
        
        # Update budget display and pie chart
        self._update_budget_display()
    
    def _check_compatibility(self):
        """Run compatibility check and display results"""
        results = run_full_check(self.selected_parts)
        
        self.compat_text.config(state="normal")
        self.compat_text.delete("1.0", tk.END)
        
        all_ok = True
        for rule_id, passed, message in results:
            status = "OK" if passed else "FAIL"
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
            self.compat_text.insert(tk.END, "\nAll compatibility checks passed!")
        else:
            self.compat_text.insert(tk.END, "\nSome compatibility issues detected")
        
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
                
                ttk.Label(share_dialog, text=f"Build '{name}' saved successfully!", 
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
                    copy_btn.config(text="Copied!")
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
        
        # Draw pie chart with adjusted dimensions
        center_x = center_y = 90
        radius = 70
        start_angle = 0
        
        # If no budget is set, just show component allocation
        if budget_value == 0:
            if total_cost == 0:
                # No parts selected and no budget - show message
                self.pie_canvas.create_text(
                    90, 90,
                    text="Set a budget\nand add components",
                    font=("Arial", 9),
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
        inner_radius = 30
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
                font=("Arial", 10, "bold"),
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
                font=("Arial", 10, "bold"),
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
            # Enable the rounded button (canvas)
            if hasattr(self.save_btn, 'configure'):
                self.save_btn.configure(state="normal")
        else:
            # Disable or update the rounded button
            if hasattr(self.save_btn, 'configure'):
                self.save_btn.configure(state="disabled")
        
        self._update_summary()
