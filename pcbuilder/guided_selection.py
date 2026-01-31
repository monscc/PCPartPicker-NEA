# Guided component selection with user-friendly questions
# No technical knowledge required
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Callable, Any
from .database_manager import get_database_manager
from .filters import component_filters
from .merge_sort import merge_sort_parts_by_price


class GuidedSelector:
    # Guided component selector with question-based filtering
    
    def __init__(self):
        self.questions = self._initialize_questions()
    
    def _initialize_questions(self) -> Dict[str, List[Dict]]:
        # Initialize user-friendly questions for each component
        return {
            "CPU": [
                {
                    "question": "What will you primarily use this PC for?",
                    "options": {
                        "Gaming": ["6_cores"],
                        "Video Editing / 3D Work": ["8_cores"],
                        "High-End Workstation": ["12_cores"],
                        "Office Work / Browsing": []
                    }
                },
                {
                    "question": "Do you plan to overclock (push performance beyond factory settings)?",
                    "options": {
                        "Yes, I want maximum performance": ["unlocked"],
                        "No, standard performance is fine": []
                    }
                },
                {
                    "question": "Do you need a dedicated graphics card, or will you use integrated graphics?",
                    "options": {
                        "I'm buying a separate graphics card": [],
                        "I'll use integrated graphics (no separate GPU)": ["integrated_gpu"]
                    }
                }
            ],
            
            "Motherboard": [
                {
                    "question": "What size case do you prefer?",
                    "options": {
                        "Full size (most expandable)": ["atx"],
                        "Compact (smaller desk footprint)": ["micro_atx"],
                        "Mini (very small, portable)": ["mini_itx"]
                    }
                },
                {
                    "question": "Do you need built-in WiFi?",
                    "options": {
                        "Yes, I'll connect wirelessly": ["wifi"],
                        "No, I'll use ethernet cable": []
                    }
                },
                {
                    "question": "Which type of RAM do you prefer?",
                    "options": {
                        "Latest generation (DDR5 - faster, more expensive)": ["ddr5"],
                        "Current generation (DDR4 - good value)": ["ddr4"],
                        "Either is fine": []
                    }
                }
            ],
            
            "RAM": [
                {
                    "question": "What will you use this PC for?",
                    "options": {
                        "Gaming only": ["16gb"],
                        "Gaming + Multitasking": ["32gb"],
                        "Content Creation / Heavy Workloads": ["32gb"],
                        "Basic use (browsing, office)": []
                    }
                },
                {
                    "question": "Which generation do you want?",
                    "options": {
                        "Latest (DDR5 - faster)": ["ddr5"],
                        "Current (DDR4 - better value)": ["ddr4"]
                    }
                },
                {
                    "question": "Do you want RGB lighting?",
                    "options": {
                        "Yes, I love RGB!": ["rgb"],
                        "No, just performance": []
                    }
                }
            ],
            
            "GPU": [
                {
                    "question": "What resolution will you game at?",
                    "options": {
                        "1080p (Full HD)": ["8gb_vram"],
                        "1440p (2K)": ["12gb_vram"],
                        "4K (Ultra HD)": ["16gb_vram"],
                        "Not for gaming": []
                    }
                },
                {
                    "question": "Which brand do you prefer?",
                    "options": {
                        "NVIDIA (DLSS, ray tracing)": ["nvidia"],
                        "AMD (good value)": ["amd"],
                        "No preference": []
                    }
                },
                {
                    "question": "Do you want ray tracing support (realistic lighting)?",
                    "options": {
                        "Yes, I want the best graphics": ["ray_tracing"],
                        "No, standard graphics are fine": []
                    }
                }
            ],
            
            "PSU": [
                {
                    "question": "What's your build type?",
                    "options": {
                        "Budget build (basic components)": ["650w"],
                        "Mid-range gaming": ["750w"],
                        "High-end / enthusiast": ["850w"]
                    }
                },
                {
                    "question": "How important is cable management?",
                    "options": {
                        "Very important (clean look)": ["modular"],
                        "Somewhat important": ["semi_modular"],
                        "Not important": ["non_modular"]
                    }
                },
                {
                    "question": "How efficient should it be?",
                    "options": {
                        "Very efficient (lower electricity bills)": ["80plus_platinum"],
                        "Standard efficiency": ["80plus_gold"],
                        "Basic": []
                    }
                }
            ],
            
            "Case": [
                {
                    "question": "What size case do you want?",
                    "options": {
                        "Full size (most room)": ["atx"],
                        "Medium (good balance)": ["micro_atx"],
                        "Small (compact)": ["mini_itx"]
                    }
                },
                {
                    "question": "Do you want a glass side panel to show off your build?",
                    "options": {
                        "Yes, tempered glass": ["tempered_glass"],
                        "No, solid panel is fine": []
                    }
                },
                {
                    "question": "What's more important to you?",
                    "options": {
                        "Best airflow (cooler, quieter)": ["mesh"],
                        "RGB lighting (looks cool)": ["rgb"],
                        "Both are fine": []
                    }
                }
            ],
            
            "Storage": [
                {
                    "question": "What's your primary use?",
                    "options": {
                        "Operating system + programs": ["ssd", "nvme", "500gb"],
                        "Gaming library": ["ssd", "1tb"],
                        "Large file storage": ["2tb"],
                        "Budget mass storage": ["hdd", "2tb"]
                    }
                },
                {
                    "question": "How fast do you need it?",
                    "options": {
                        "Fastest possible (for OS/games)": ["nvme", "pcie4"],
                        "Fast enough": ["ssd"],
                        "Storage space over speed": ["hdd"]
                    }
                },
                {
                    "question": "How much storage do you need?",
                    "options": {
                        "500GB - 1TB": ["500gb"],
                        "1TB - 2TB": ["1tb"],
                        "2TB+": ["2tb"]
                    }
                }
            ],
            
            "Cooler": [
                {
                    "question": "What type of cooler do you prefer?",
                    "options": {
                        "Air cooler (reliable, quiet)": ["air"],
                        "Liquid cooler (better cooling, looks cool)": ["aio"]
                    }
                },
                {
                    "question": "How powerful is your CPU?",
                    "options": {
                        "Budget / Mid-range": ["120mm"],
                        "High-end / Gaming": ["240mm"],
                        "Enthusiast / Overclocked": ["240mm"]
                    }
                },
                {
                    "question": "Do you want RGB lighting?",
                    "options": {
                        "Yes, RGB all the things!": ["rgb"],
                        "No, just cooling performance": ["quiet"]
                    }
                }
            ]
        }
    
    def get_questions(self, category: str) -> List[Dict]:
        # Get questions for a specific component category
        return self.questions.get(category, [])


class GuidedSelectorDialog(tk.Toplevel):
    # Dialog for guided component selection
    
    def __init__(self, parent, category: str, on_select_callback):
        super().__init__(parent)
        
        self.category = category
        self.on_select_callback = on_select_callback
        self.guided_selector = GuidedSelector()
        self.answers = {}
        self.active_filters = []
        
        self.title(f"Choose {category} - Guided Selection")
        self.geometry("700x600")
        self.transient(parent)
        
        self._create_widgets()
        
        # Grab focus after window is created and visible
        self.update_idletasks()
        self.grab_set()
    
    def _create_widgets(self):
        # Create the dialog interface
        # Header
        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill="x")
        
        ttk.Label(header_frame, 
                 text=f"Let's find the perfect {self.category} for you!",
                 font=("Arial", 14, "bold")).pack()
        
        ttk.Label(header_frame,
                 text="Answer a few simple questions - no technical knowledge needed",
                 font=("Arial", 9),
                 foreground="#666").pack(pady=5)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        
        # Questions area
        questions_container = ttk.Frame(self)
        questions_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollable questions
        canvas = tk.Canvas(questions_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(questions_container, orient="vertical", command=canvas.yview)
        self.questions_frame = ttk.Frame(canvas)
        
        self.questions_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Build questions
        self._build_questions()
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        ttk.Button(button_frame, text="Show Results", 
                  command=self._show_results,
                  style="Accent.TButton").pack(side="right", padx=5)
        
        ttk.Button(button_frame, text="Cancel",
                  command=self.destroy).pack(side="right", padx=5)
        
        ttk.Button(button_frame, text="Reset Answers",
                  command=self._reset_answers).pack(side="left", padx=5)
    
    def _build_questions(self):
        # Build the question interface
        questions = self.guided_selector.get_questions(self.category)
        
        if not questions:
            ttk.Label(self.questions_frame,
                     text="No guided questions available for this component.",
                     font=("Arial", 10)).pack(pady=20)
            return
        
        for i, q in enumerate(questions, start=1):
            # Question frame
            q_frame = ttk.LabelFrame(self.questions_frame, 
                                     text=f"Question {i}",
                                     padding=15)
            q_frame.pack(fill="x", pady=10)
            
            # Question text
            ttk.Label(q_frame,
                     text=q["question"],
                     font=("Arial", 10, "bold"),
                     wraplength=600).pack(anchor="w", pady=(0, 10))
            
            # Options
            var = tk.StringVar(value="")
            self.answers[i] = {"var": var, "filters_map": q["options"]}
            
            for option_text in q["options"].keys():
                rb = ttk.Radiobutton(q_frame,
                                    text=option_text,
                                    variable=var,
                                    value=option_text)
                rb.pack(anchor="w", pady=3, padx=20)
    
    def _reset_answers(self):
        # Reset all answers
        for answer_data in self.answers.values():
            answer_data["var"].set("")
    
    def _show_results(self):
        # Show filtered results based on answers
        # Collect active filters
        self.active_filters = []
        
        for answer_data in self.answers.values():
            selected = answer_data["var"].get()
            if selected:
                filters = answer_data["filters_map"].get(selected, [])
                self.active_filters.extend(filters)
        
        # Remove duplicates
        self.active_filters = list(set(self.active_filters))
        
        # Get all parts for this category
        db = get_database_manager()
        components = db.get_all_components()
        all_parts = [comp.to_dict() for comp in components]
        category_parts = [p for p in all_parts if p["category"] == self.category]
        
        # Apply filters
        if self.active_filters:
            filtered_parts = component_filters.apply_filters(
                category_parts,
                self.category,
                self.active_filters
            )
        else:
            filtered_parts = category_parts
        
        # Show results dialog
        self._show_results_dialog(filtered_parts)
    
    def _show_results_dialog(self, parts: List[Dict]):
        # Show filtered results in a selection dialog
        results_dialog = tk.Toplevel(self)
        results_dialog.title(f"Select {self.category}")
        results_dialog.geometry("800x550")
        results_dialog.transient(self)
        
        # Header
        header_frame = ttk.Frame(results_dialog, padding=10)
        header_frame.pack(fill="x")
        
        if parts:
            ttk.Label(header_frame,
                     text=f"Found {len(parts)} {self.category}(s) matching your needs",
                     font=("Arial", 12, "bold")).pack()
        else:
            ttk.Label(header_frame,
                     text=f"No {self.category} found with those requirements",
                     font=("Arial", 12, "bold"),
                     foreground="red").pack()
            
            ttk.Label(header_frame,
                     text="Try adjusting your answers or browse all components",
                     font=("Arial", 9)).pack()
        
        # Sort controls frame (NEW)
        sort_frame = ttk.Frame(results_dialog, padding=(10, 5))
        sort_frame.pack(fill="x")
        
        # Track sort state
        sort_state = {"ascending": None}  # None = unsorted, True = ascending, False = descending
        
        sort_label = ttk.Label(sort_frame, text="Not sorted", foreground="#666", font=("Arial", 9))
        sort_label.pack(side="left", padx=10)
        
        # Results list
        list_frame = ttk.Frame(results_dialog)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ... rest of the code ...
        
        # Grab focus after everything is created
        results_dialog.update_idletasks()
        results_dialog.grab_set()
        
        # Treeview
        columns = ("name", "price")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        tree.heading("name", text="Component Name")
        tree.heading("price", text="Price")
        
        tree.column("name", width=600)
        tree.column("price", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Store original parts list
        current_parts = parts.copy()
        
        # Function to populate tree with current parts list
        def populate_tree(parts_list):
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Add parts to tree
            for part in parts_list:
                tree.insert("", tk.END, values=(
                    part["name"],
                    f"£{part['price']:.2f}"
                ), tags=(part["id"],))
        
        # Initially populate with unsorted parts
        populate_tree(current_parts)
        
        # Sort button handler
        def sort_by_price():
            nonlocal current_parts
            
            if sort_state["ascending"] is None:
                # First click: Sort ascending (low to high)
                current_parts = merge_sort_parts_by_price(parts, ascending=True)
                sort_state["ascending"] = True
                sort_label.config(
                    text="Sorted by price: Low → High",
                    foreground="#4CAF50"
                )
            elif sort_state["ascending"] is True:
                # Second click: Sort descending (high to low)
                current_parts = merge_sort_parts_by_price(parts, ascending=False)
                sort_state["ascending"] = False
                sort_label.config(
                    text="Sorted by price: High → Low",
                    foreground="#2196F3"
                )
            else:
                # Third click: Reset to unsorted
                current_parts = parts.copy()
                sort_state["ascending"] = None
                sort_label.config(
                    text="Not sorted",
                    foreground="#666"
                )
            
            # Repopulate tree with sorted list
            populate_tree(current_parts)
        
        # Sort button
        sort_btn = ttk.Button(sort_frame, 
                             text="💰 Sort by Price",
                             command=sort_by_price)
        sort_btn.pack(side="right", padx=10)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        btn_frame = ttk.Frame(results_dialog)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def select_part():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a component")
                return
            
            # Get part ID from tags
            item = selection[0]
            part_id = tree.item(item)["tags"][0]
            
            # Find the part
            selected_part = next((p for p in parts if p["id"] == part_id), None)
            
            if selected_part:
                self.on_select_callback(selected_part)
                results_dialog.destroy()
                self.destroy()
        
        def show_all():
            # Show all components without filters
            db = get_database_manager()
            components = db.get_all_components()
            all_parts = [comp.to_dict() for comp in components]
            category_parts = [p for p in all_parts if p["category"] == self.category]
            results_dialog.destroy()
            self._show_results_dialog(category_parts)
        
        ttk.Button(btn_frame, text="Select",
                  command=select_part).pack(side="right", padx=5)
        
        ttk.Button(btn_frame, text="Cancel",
                  command=results_dialog.destroy).pack(side="right", padx=5)
        
        if self.active_filters:  # Only show if filters were applied
            ttk.Button(btn_frame, text="Show All Components",
                      command=show_all).pack(side="left", padx=5)
        
        # Double-click to select
        tree.bind("<Double-Button-1>", lambda e: select_part())
        
        # Grab focus after everything is created
        results_dialog.update_idletasks()
        results_dialog.grab_set()


# Global instance
guided_selector = GuidedSelector()
