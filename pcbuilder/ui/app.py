# Main Tkinter application entry point
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from .views.login_frame import LoginFrame
from .views.main_frame import MainFrame
from ..database_manager import get_database_manager


class PCBuilderApp(tk.Tk):
    # Main application window
    
    def __init__(self):
        super().__init__()
        
        self.title("PC Part Picker - NEA Project")
        self.geometry("1400x900")
        
        # Modern styling
        self._apply_modern_theme()
        
        # Initialize database (auto-initialized by DatabaseManager)
        self._load_sample_data_if_needed()
        
        # User session
        self.current_user_id = None
        self.current_username = None
        self.current_user_role = None
        
        # Container for frames
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        
        # Initialize frames
        for F in (LoginFrame, MainFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Show login frame first
        self.show_frame("LoginFrame")
    
    def _apply_modern_theme(self):
        # Apply modern color scheme and styling
        style = ttk.Style()
        
        # Use 'clam' theme as base for better customization
        style.theme_use('clam')
        
        # Modern vibrant color palette
        bg_color = "#e8f4f8"  # Light blue-gray background
        primary_color = "#2196F3"  # Vibrant blue
        primary_hover = "#1976D2"  # Darker blue for hover
        accent_color = "#4CAF50"  # Vibrant green accent
        warning_color = "#FF9800"  # Orange
        danger_color = "#F44336"  # Red
        purple_color = "#9C27B0"  # Purple
        text_color = "#1c1e21"  # Dark text
        secondary_text = "#5f6368"  # Gray text
        border_color = "#b0bec5"  # Light border
        white = "#ffffff"
        card_bg = "#ffffff"  # White cards
        
        # Configure root window
        self.configure(bg=bg_color)
        
        # Frame styling with colors
        style.configure("TFrame", background=bg_color)
        style.configure("Card.TFrame", background=card_bg, relief="flat")
        style.configure("Accent.TFrame", background=primary_color)
        
        # Label styling
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=primary_color)
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12, "bold"), foreground=text_color)
        style.configure("Secondary.TLabel", foreground=secondary_text, font=("Segoe UI", 9))
        style.configure("Success.TLabel", foreground=accent_color, font=("Segoe UI", 10, "bold"))
        style.configure("Warning.TLabel", foreground=warning_color, font=("Segoe UI", 10, "bold"))
        style.configure("Error.TLabel", foreground=danger_color, font=("Segoe UI", 10, "bold"))
        
        # Button styling - Modern flat design with vibrant colors and rounded appearance
        style.configure("TButton",
                       background=white,
                       foreground=text_color,
                       borderwidth=0,
                       focuscolor="none",
                       relief="flat",
                       padding=(16, 10),
                       font=("Segoe UI", 10))
        style.map("TButton",
                 background=[("active", "#f5f5f5"), ("pressed", "#e0e0e0")],
                 relief=[("pressed", "flat")])
        
        # Accent button (primary action) - Vibrant blue with more padding for rounded look
        style.configure("Accent.TButton",
                       background=primary_color,
                       foreground=white,
                       borderwidth=0,
                       relief="flat",
                       padding=(18, 12),
                       font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                 background=[("active", primary_hover), ("pressed", primary_hover)])
        
        # Success button - Vibrant green with rounded appearance
        style.configure("Success.TButton",
                       background=accent_color,
                       foreground=white,
                       borderwidth=0,
                       relief="flat",
                       padding=(16, 10),
                       font=("Segoe UI", 10, "bold"))
        style.map("Success.TButton",
                 background=[("active", "#45a049"), ("pressed", "#45a049")])
        
        # Warning button - Orange with rounded appearance
        style.configure("Warning.TButton",
                       background=warning_color,
                       foreground=white,
                       borderwidth=0,
                       relief="flat",
                       padding=(16, 10),
                       font=("Segoe UI", 10, "bold"))
        style.map("Warning.TButton",
                 background=[("active", "#FB8C00"), ("pressed", "#FB8C00")])
        
        # Danger button - Red with rounded appearance
        style.configure("Danger.TButton",
                       background=danger_color,
                       foreground=white,
                       borderwidth=0,
                       relief="flat",
                       padding=(16, 10),
                       font=("Segoe UI", 10))
        style.map("Danger.TButton",
                 background=[("active", "#E53935"), ("pressed", "#E53935")])
        
        # Purple button with rounded appearance
        style.configure("Purple.TButton",
                       background=purple_color,
                       foreground=white,
                       borderwidth=0,
                       relief="flat",
                       padding=(16, 10),
                       font=("Segoe UI", 10, "bold"))
        style.map("Purple.TButton",
                 background=[("active", "#8E24AA"), ("pressed", "#8E24AA")])
        
        # LabelFrame styling with colorful borders
        style.configure("TLabelframe", background=white, borderwidth=2, relief="solid", bordercolor=border_color)
        style.configure("TLabelframe.Label", background=white, foreground=primary_color, 
                       font=("Segoe UI", 11, "bold"))
        
        # Special colored label frames
        style.configure("Primary.TLabelframe", bordercolor=primary_color, borderwidth=2)
        style.configure("Primary.TLabelframe.Label", foreground=primary_color)
        
        style.configure("Success.TLabelframe", bordercolor=accent_color, borderwidth=2)
        style.configure("Success.TLabelframe.Label", foreground=accent_color)
        
        style.configure("Warning.TLabelframe", bordercolor=warning_color, borderwidth=2)
        style.configure("Warning.TLabelframe.Label", foreground=warning_color)
        
        # Entry styling
        style.configure("TEntry",
                       fieldbackground=white,
                       foreground=text_color,
                       borderwidth=1,
                       relief="solid",
                       padding=8)
        
        # Notebook (tabs) styling
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab",
                       background=white,
                       foreground=text_color,
                       padding=(20, 10),
                       font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                 background=[("selected", primary_color)],
                 foreground=[("selected", white)])
    
    def _load_sample_data_if_needed(self):
        # Load sample parts if database is empty
        db = get_database_manager()
        components = db.get_all_components()
        if len(components) == 0:
            sample_path = Path(__file__).resolve().parents[2] / "data" / "sample_parts.json"
            if sample_path.exists():
                db.load_components_from_json(sample_path)
                print("Loaded sample parts data")
    
    def show_frame(self, frame_name):
        # Show a frame for the given frame name
        frame = self.frames[frame_name]
        frame.tkraise()
        # Refresh frame if it has a refresh method
        if hasattr(frame, 'on_show'):
            frame.on_show()
    
    def login_user(self, user_id, username, role=None):
        # Set current user and show main frame
        self.current_user_id = user_id
        self.current_username = username
        self.current_user_role = role
        self.show_frame("MainFrame")
    
    def logout_user(self):
        # Clear current user and show login frame
        from ..auth import session
        session.logout()
        self.current_user_id = None
        self.current_username = None
        self.current_user_role = None
        self.show_frame("LoginFrame")


def main():
    # Entry point for GUI application
    app = PCBuilderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
