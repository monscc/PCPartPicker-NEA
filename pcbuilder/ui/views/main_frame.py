"""Main application frame with tabbed interface and role-based access"""
import tkinter as tk
from tkinter import ttk, messagebox
from .builder_tab import BuilderTab
from .builds_tab import BuildsTab
from .tracker_tab import TrackerTab
from .guide_tab import GuideTab
from ...auth import session, UserRole


class MainFrame(ttk.Frame):
    """Main frame with tabbed interface"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Top bar with username and logout
        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", padx=10, pady=5)
        
        self.username_label = ttk.Label(top_bar, text="", font=("Arial", 10))
        self.username_label.pack(side="left")
        
        # Role indicator
        self.role_label = ttk.Label(top_bar, text="", font=("Arial", 9), foreground="blue")
        self.role_label.pack(side="left", padx=10)
        
        logout_btn = ttk.Button(top_bar, text="Logout", command=self._logout)
        logout_btn.pack(side="right")
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create tabs
        self.builder_tab = BuilderTab(self.notebook, controller)
        self.builds_tab = BuildsTab(self.notebook, controller)
        self.tracker_tab = TrackerTab(self.notebook, controller)
        self.guide_tab = GuideTab(self.notebook)
        
        self.notebook.add(self.builder_tab, text="Build PC")
        self.notebook.add(self.builds_tab, text="My Builds")
        self.notebook.add(self.tracker_tab, text="Price Tracker")
        self.notebook.add(self.guide_tab, text="📚 PC Guide")
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
    
    def _logout(self):
        """Handle logout"""
        self.controller.logout_user()
    
    def _on_tab_change(self, event):
        """Handle tab change"""
        selected_tab = self.notebook.select()
        tab_index = self.notebook.index(selected_tab)
        
        # Refresh the selected tab
        if tab_index == 1:  # Builds tab
            self.builds_tab.refresh()
        elif tab_index == 2:  # Tracker tab
            self.tracker_tab.refresh()
        # Guide tab (index 3) doesn't need refresh - it's static content
    
    def on_show(self):
        """Called when frame is shown"""
        username = self.controller.current_username or "User"
        role = self.controller.current_user_role or UserRole.GUEST
        
        # Display username and role
        self.username_label.config(text=f"Logged in as: {username}")
        
        # Role indicator with icon
        role_icons = {
            UserRole.GUEST: "🔓",
            UserRole.STANDARD: "👤",
            UserRole.PREMIUM: "⭐",
            UserRole.ADMIN: "🔑"
        }
        icon = role_icons.get(role, "")
        self.role_label.config(text=f"{icon} {role.name.capitalize()}")
        
        # Configure tab access based on role
        current_user = session.get_current_user()
        if current_user:
            # Hide "My Builds" tab for guests
            if current_user.is_guest():
                self.notebook.tab(1, state="disabled")
                # Show info message
                if not hasattr(self, '_guest_warning_shown'):
                    messagebox.showinfo(
                        "Guest Mode",
                        "You're using Guest mode.\n\n"
                        "✓ You can build and check compatibility\n"
                        "✗ You cannot save or load builds\n\n"
                        "Create an account to save your builds!"
                    )
                    self._guest_warning_shown = True
            else:
                self.notebook.tab(1, state="normal")
                self._guest_warning_shown = False
        
        # Switch to build tab and refresh
        self.notebook.select(0)
        self.builder_tab.refresh()
