"""Price tracker tab with chart visualization"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ...db import list_parts
from ...price_tracker import record_price, get_price_history


class TrackerTab(ttk.Frame):
    """Price tracker tab for viewing price history"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.current_part_id = None
        self.figure = None
        self.canvas = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the price tracker interface"""
        # Top controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(control_frame, text="Select Part:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.part_combo = ttk.Combobox(control_frame, state="readonly", width=50)
        self.part_combo.pack(side="left", padx=5)
        self.part_combo.bind("<<ComboboxSelected>>", self._on_part_selected)
        
        ttk.Button(control_frame, text="View Price History", command=self._view_history).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Add Sample Data", command=self._add_sample_data).pack(side="left", padx=5)
        
        # Chart area
        chart_frame = ttk.LabelFrame(self, text="Price History Chart")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Info text
        info_frame = ttk.LabelFrame(self, text="Price Information")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_text = tk.Text(info_frame, height=5, wrap="word")
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._show_welcome_message()
    
    def _show_welcome_message(self):
        """Show welcome message in chart area"""
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, "Select a part to view price history", 
                ha='center', va='center', fontsize=14, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
    
    def _on_part_selected(self, event=None):
        """Handle part selection"""
        selection = self.part_combo.get()
        if not selection:
            return
        
        # Extract part ID from selection (format: "Part Name (id)")
        if " (" in selection and selection.endswith(")"):
            self.current_part_id = selection.split(" (")[-1][:-1]
        else:
            self.current_part_id = None
    
    def _view_history(self):
        """View price history for selected part"""
        if not self.current_part_id:
            messagebox.showwarning("No Selection", "Please select a part first")
            return
        
        history = get_price_history(self.current_part_id, limit=100)
        
        if not history:
            messagebox.showinfo("No Data", "No price history available for this part.\nUse 'Add Sample Data' to generate some.")
            return
        
        # Update info text
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"Part ID: {self.current_part_id}\n")
        self.info_text.insert(tk.END, f"Data Points: {len(history)}\n")
        
        if history:
            prices = [h["price"] for h in history]
            current_price = prices[0]
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            self.info_text.insert(tk.END, f"Current Price: £{current_price:.2f}\n")
            self.info_text.insert(tk.END, f"Min: £{min_price:.2f} | Max: £{max_price:.2f} | Avg: £{avg_price:.2f}\n")
        
        # Plot the chart
        self._plot_history(history)
    
    def _plot_history(self, history):
        """Plot price history chart"""
        if not history:
            return
        
        # Clear previous plot
        self.figure.clear()
        
        # Reverse to show oldest first
        history = list(reversed(history))
        
        dates = [datetime.fromisoformat(h["timestamp"]) for h in history]
        prices = [h["price"] for h in history]
        
        ax = self.figure.add_subplot(111)
        ax.plot(dates, prices, marker='o', linestyle='-', linewidth=2, markersize=6, color='#2E86AB')
        
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Price (£)', fontsize=11)
        ax.set_title(f'Price History: {self.current_part_id}', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis dates
        self.figure.autofmt_xdate()
        
        # Tight layout to prevent label cutoff
        self.figure.tight_layout()
        
        self.canvas.draw()
    
    def _add_sample_data(self):
        """Add sample price data for the selected part"""
        if not self.current_part_id:
            messagebox.showwarning("No Selection", "Please select a part first")
            return
        
        # Generate sample price data (random walk)
        import random
        base_price = 149.99
        now = datetime.now()
        
        for i in range(30):  # 30 days of data
            timestamp = (now - timedelta(days=29-i)).isoformat()
            # Random price variation
            price_change = random.uniform(-8, 8)
            base_price = max(40, base_price + price_change)  # Don't go below £40
            record_price(self.current_part_id, round(base_price, 2), timestamp)
        
        messagebox.showinfo("Success", f"Added 30 days of sample price data for {self.current_part_id}")
        self._view_history()
    
    def refresh(self):
        """Refresh the parts list"""
        parts = list_parts()
        
        # Format: "Part Name (id)"
        part_options = [f"{p['name']} ({p['id']})" for p in parts]
        self.part_combo["values"] = part_options
        
        if part_options:
            self.part_combo.set(part_options[0])
            self._on_part_selected()
