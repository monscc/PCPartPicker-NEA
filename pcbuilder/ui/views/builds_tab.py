"""Saved builds tab with template builds"""
import tkinter as tk
from tkinter import ttk, messagebox
from ...db import load_user_builds, load_build_by_id, import_build_from_share_key
from ...compat import run_full_check
from ...templates import get_template_builds, get_template_summary


class BuildsTab(ttk.Frame):
    """Saved builds tab for viewing and loading builds"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the builds list interface"""
        # Top label
        ttk.Label(self, text="My Saved Builds", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Import Build Section (at the top)
        import_frame = ttk.LabelFrame(self, text="🔑 Import Build from Share Key")
        import_frame.pack(fill="x", padx=10, pady=5)
        
        import_row = ttk.Frame(import_frame)
        import_row.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(import_row, text="Enter Share Key:", font=("Arial", 9)).pack(side="left", padx=5)
        
        self.share_key_var = tk.StringVar()
        share_key_entry = ttk.Entry(import_row, textvariable=self.share_key_var, 
                                    width=12, font=("Courier", 11))
        share_key_entry.pack(side="left", padx=5)
        
        ttk.Button(import_row, text="Import Build", 
                  command=self._import_build).pack(side="left", padx=5)
        
        ttk.Label(import_row, text="(Enter an 8-character key to import someone else's build)", 
                 font=("Arial", 8), foreground="#666").pack(side="left", padx=10)
        
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=10, pady=5)
        
        # Template Builds Section
        template_frame = ttk.LabelFrame(self, text="📋 Template Builds (Available to All Users)")
        template_frame.pack(fill="x", padx=10, pady=5)
        
        templates = get_template_builds()
        for template_id, template in templates.items():
            summary = get_template_summary(template_id)
            
            template_row = ttk.Frame(template_frame)
            template_row.pack(fill="x", padx=5, pady=3)
            
            # Template info
            info_text = f"{summary['name']} - {summary['target_price']}"
            ttk.Label(template_row, text=info_text, width=50, anchor="w").pack(side="left")
            
            # View button
            ttk.Button(
                template_row, 
                text="View", 
                command=lambda tid=template_id: self._view_template(tid),
                width=10
            ).pack(side="right", padx=2)
        
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=10, pady=10)
        
        # Builds list
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for builds list
        columns = ("id", "name", "created", "parts_count", "total_price", "share_key")
        self.builds_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.builds_tree.heading("id", text="ID")
        self.builds_tree.heading("name", text="Build Name")
        self.builds_tree.heading("created", text="Created")
        self.builds_tree.heading("parts_count", text="Parts")
        self.builds_tree.heading("total_price", text="Total Price")
        self.builds_tree.heading("share_key", text="Share Key")
        
        self.builds_tree.column("id", width=50)
        self.builds_tree.column("name", width=200)
        self.builds_tree.column("created", width=150)
        self.builds_tree.column("parts_count", width=60)
        self.builds_tree.column("total_price", width=100)
        self.builds_tree.column("share_key", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.builds_tree.yview)
        self.builds_tree.configure(yscrollcommand=scrollbar.set)
        
        self.builds_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click to view build
        self.builds_tree.bind("<Double-Button-1>", self._on_build_double_click)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="View Details", command=self._view_build).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Load to Builder", command=self._load_to_builder).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh).pack(side="left", padx=5)
    
    def refresh(self):
        """Refresh the builds list"""
        # Clear existing items
        for item in self.builds_tree.get_children():
            self.builds_tree.delete(item)
        
        if not self.controller.current_user_id:
            return
        
        # Load builds
        builds = load_user_builds(self.controller.current_user_id)
        
        for build in builds:
            parts = build.get("parts", {})
            parts_count = sum(1 for p in parts.values() if p is not None)
            total_price = sum(p.get("price", 0) for p in parts.values() if p is not None)
            
            self.builds_tree.insert("", tk.END, values=(
                build["id"],
                build["name"],
                build["created_at"][:19],  # Trim microseconds
                parts_count,
                f"£{total_price:.2f}",
                build.get("share_key", "N/A")
            ))
    
    def _on_build_double_click(self, event):
        """Handle double-click on build"""
        self._view_build()
    
    def _view_build(self):
        """View build details in a popup"""
        selection = self.builds_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a build to view")
            return
        
        item = self.builds_tree.item(selection[0])
        build_id = item["values"][0]
        
        build = load_build_by_id(build_id)
        if not build:
            messagebox.showerror("Error", "Build not found")
            return
        
        # Create details window
        details = tk.Toplevel(self)
        details.title(f"Build Details - {build['name']}")
        details.geometry("600x500")
        details.transient(self)
        
        # Build info
        info_frame = ttk.Frame(details)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"Name: {build['name']}", font=("Arial", 12, "bold")).pack(anchor="w")
        ttk.Label(info_frame, text=f"Created: {build['created_at'][:19]}").pack(anchor="w")
        
        # Parts list
        parts_frame = ttk.LabelFrame(details, text="Components")
        parts_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        parts_text = tk.Text(parts_frame, height=15, wrap="word")
        parts_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        total_price = 0.0
        for category, part in build["parts"].items():
            if part:
                price = part.get("price", 0)
                total_price += price
                parts_text.insert(tk.END, f"{category}: {part['name']} (£{price:.2f})\n")
                
                # Show key attributes
                attrs = part.get("attributes", {})
                for key, value in attrs.items():
                    if value:
                        parts_text.insert(tk.END, f"  • {key}: {value}\n")
            else:
                parts_text.insert(tk.END, f"{category}: (Not selected)\n")
        
        parts_text.insert(tk.END, f"\nTotal Price: £{total_price:.2f}")
        parts_text.config(state="disabled")
        
        # Compatibility check
        compat_frame = ttk.LabelFrame(details, text="Compatibility")
        compat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        compat_text = tk.Text(compat_frame, height=8, wrap="word")
        compat_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        results = run_full_check(build["parts"])
        for rule_id, passed, message in results:
            status = "✓" if passed else "✗"
            compat_text.insert(tk.END, f"{status} {message}\n")
        
        compat_text.config(state="disabled")
        
        # Close button
        ttk.Button(details, text="Close", command=details.destroy).pack(pady=10)
    
    def _load_to_builder(self):
        """Load selected build to the builder tab"""
        selection = self.builds_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a build to load")
            return
        
        item = self.builds_tree.item(selection[0])
        build_id = item["values"][0]
        
        build = load_build_by_id(build_id)
        if not build:
            messagebox.showerror("Error", "Build not found")
            return
        
        # Get builder tab and load parts
        main_frame = self.controller.frames["MainFrame"]
        builder_tab = main_frame.builder_tab
        
        # Load each part
        for category, part in build["parts"].items():
            if part and category in builder_tab.selected_parts:
                builder_tab.selected_parts[category] = part
                # Update the label display (not combo.set anymore)
                label = builder_tab.part_combos.get(category)
                if label:
                    label.config(text=part["name"], foreground="black")
            else:
                builder_tab.selected_parts[category] = None
                # Update the label display
                label = builder_tab.part_combos.get(category)
                if label:
                    label.config(text="Not selected", foreground="#666")
        
        builder_tab._update_summary()
        
        # Switch to builder tab
        main_frame.notebook.select(0)
        
        messagebox.showinfo("Success", f"Build '{build['name']}' loaded to builder")
    
    def _view_template(self, template_id: str):
        """View template build details"""
        from ...templates import load_template_build
        
        summary = get_template_summary(template_id)
        if not summary:
            messagebox.showerror("Error", "Template not found")
            return
        
        template_parts = load_template_build(template_id)
        if not template_parts:
            messagebox.showerror("Error", "Failed to load template")
            return
        
        # Create details window
        details = tk.Toplevel(self)
        details.title(f"Template: {summary['name']}")
        details.geometry("600x600")
        details.transient(self)
        
        # Build info
        info_frame = ttk.Frame(details)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text=summary['name'], font=("Arial", 14, "bold")).pack(anchor="w")
        ttk.Label(info_frame, text=summary['description'], wraplength=550).pack(anchor="w", pady=5)
        ttk.Label(info_frame, text=f"Target Price: {summary['target_price']}", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(info_frame, text=f"Actual Price: £{summary['actual_price']:.2f}", font=("Arial", 10, "bold"), foreground="green").pack(anchor="w")
        
        # Parts list
        parts_frame = ttk.LabelFrame(details, text="Components")
        parts_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        parts_text = tk.Text(parts_frame, height=15, wrap="word")
        parts_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        for category in ["CPU", "Motherboard", "RAM", "GPU", "PSU", "Case", "Storage", "Cooler"]:
            part = template_parts.get(category)
            if part:
                price = part.get("price", 0)
                parts_text.insert(tk.END, f"{category}: {part['name']} (£{price:.2f})\n")
            else:
                parts_text.insert(tk.END, f"{category}: Not found in database\n")
        
        parts_text.config(state="disabled")
        
        # Compatibility check
        compat_frame = ttk.LabelFrame(details, text="Compatibility Check")
        compat_frame.pack(fill="both", padx=10, pady=5)
        
        compat_text = tk.Text(compat_frame, height=8, wrap="word")
        compat_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        results = run_full_check(template_parts)
        for rule_id, passed, message in results:
            status = "✓" if passed else "✗"
            compat_text.insert(tk.END, f"{status} {message}\n")
        
        compat_text.config(state="disabled")
        
        # Buttons
        btn_frame = ttk.Frame(details)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Load to Builder", 
            command=lambda: self._load_template_to_builder(template_id, details)
        ).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Close", command=details.destroy).pack(side="left", padx=5)
    
    def _load_template_to_builder(self, template_id: str, dialog=None):
        """Load template to builder tab"""
        from ...templates import load_template_build
        
        template_parts = load_template_build(template_id)
        if not template_parts:
            messagebox.showerror("Error", "Failed to load template")
            return
        
        # Get builder tab and load parts
        main_frame = self.controller.frames["MainFrame"]
        builder_tab = main_frame.builder_tab
        
        # Load each part
        for category, part in template_parts.items():
            if part and category in builder_tab.selected_parts:
                builder_tab.selected_parts[category] = part
                # Update the label display (not combo.set anymore)
                label = builder_tab.part_combos.get(category)
                if label:
                    label.config(text=part["name"], foreground="black")
            else:
                builder_tab.selected_parts[category] = None
                # Update the label display
                label = builder_tab.part_combos.get(category)
                if label:
                    label.config(text="Not selected", foreground="#666")
        
        builder_tab._update_summary()
        
        # Close dialog if provided
        if dialog:
            dialog.destroy()
        
        # Switch to builder tab
        main_frame.notebook.select(0)
        
        summary = get_template_summary(template_id)
        messagebox.showinfo("Success", f"{summary['name']} loaded to builder!")
    
    def _import_build(self):
        """Import a build using a share key"""
        share_key = self.share_key_var.get().strip().upper()
        
        if not share_key:
            messagebox.showwarning("Invalid Key", "Please enter a share key")
            return
        
        if len(share_key) != 8:
            messagebox.showwarning("Invalid Key", "Share key must be 8 characters")
            return
        
        try:
            result = import_build_from_share_key(self.controller.current_user_id, share_key)
            
            if result is None:
                messagebox.showerror("Not Found", f"No build found with share key: {share_key}")
                return
            
            build_id, new_share_key = result
            
            # Clear input
            self.share_key_var.set("")
            
            # Refresh builds list
            self.refresh()
            
            # Show success
            messagebox.showinfo(
                "Success", 
                f"Build imported successfully!\n\n"
                f"The build has been added to your saved builds.\n"
                f"Your copy's share key: {new_share_key}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import build: {str(e)}")
