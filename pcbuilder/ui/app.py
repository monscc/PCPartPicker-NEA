"""Main Tkinter application entry point"""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from .views.login_frame import LoginFrame
from .views.main_frame import MainFrame
from ..db import init_db, load_sample_parts


class PCBuilderApp(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("PC Part Picker - NEA Project")
        self.geometry("1200x800")
        
        # Initialize database
        init_db()
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
    
    def _load_sample_data_if_needed(self):
        """Load sample parts if database is empty"""
        from ..db import list_parts
        parts = list_parts()
        if len(parts) == 0:
            sample_path = Path(__file__).resolve().parents[2] / "data" / "sample_parts.json"
            if sample_path.exists():
                load_sample_parts(sample_path)
                print("Loaded sample parts data")
    
    def show_frame(self, frame_name):
        """Show a frame for the given frame name"""
        frame = self.frames[frame_name]
        frame.tkraise()
        # Refresh frame if it has a refresh method
        if hasattr(frame, 'on_show'):
            frame.on_show()
    
    def login_user(self, user_id, username, role=None):
        """Set current user and show main frame"""
        self.current_user_id = user_id
        self.current_username = username
        self.current_user_role = role
        self.show_frame("MainFrame")
    
    def logout_user(self):
        """Clear current user and show login frame"""
        from ..auth import session
        session.logout()
        self.current_user_id = None
        self.current_username = None
        self.current_user_role = None
        self.show_frame("LoginFrame")


def main():
    """Entry point for GUI application"""
    app = PCBuilderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
