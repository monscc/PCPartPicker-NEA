# Login and registration frame with multi-level access control
import tkinter as tk
from tkinter import ttk, messagebox
from ...auth import session, UserRole
from ...database_manager import get_database_manager


def register(username: str, password: str) -> tuple[bool, str]:
    # Register a new user
    db = get_database_manager()
    try:
        user_id = db.create_user(username, password, role=1)
        if user_id:
            return True, "Account created successfully"
        return False, "Username already exists"
    except ValueError as e:
        return False, str(e)


def authenticate(username: str, password: str) -> tuple[bool, tuple | None, str]:
    # Authenticate a user
    db = get_database_manager()
    result = db.authenticate_user(username, password)
    if result:
        user_id, role = result
        return True, (user_id, role), "Login successful"
    return False, None, "Invalid username or password"


class LoginFrame(ttk.Frame):
    # Login/Registration frame
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Center container
        center = ttk.Frame(self)
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ttk.Label(center, text="PC Part Picker", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        ttk.Label(center, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(center, width=25)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        ttk.Label(center, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(center, width=25, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(center)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.login_btn = ttk.Button(button_frame, text="Login", command=self._login, width=12)
        self.login_btn.grid(row=0, column=0, padx=5)
        
        self.register_btn = ttk.Button(button_frame, text="Register", command=self._register, width=12)
        self.register_btn.grid(row=0, column=1, padx=5)
        
        # Guest access button
        guest_frame = ttk.Frame(center)
        guest_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Separator(guest_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Label(guest_frame, text="Don't have an account?", font=("Arial", 9)).pack()
        self.guest_btn = ttk.Button(
            guest_frame, 
            text="Continue as Guest", 
            command=self._continue_as_guest, 
            width=20
        )
        self.guest_btn.pack(pady=5)
        
        guest_info = ttk.Label(
            guest_frame, 
            text="(Guest mode: Full builder access, but cannot save builds)",
            font=("Arial", 8),
            foreground="gray"
        )
        guest_info.pack()
        
        # Status label
        self.status_label = ttk.Label(center, text="", foreground="red")
        self.status_label.grid(row=5, column=0, columnspan=2)
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self._login())
        self.password_entry.bind("<Return>", lambda e: self._login())
    
    def _login(self):
        # Handle login button click
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="Please enter username and password")
            return
        
        success, result, message = authenticate(username, password)
        if success:
            user_id, role = result  # Unpack user_id and role
            self.status_label.config(text="Login successful!", foreground="green")
            
            # Set up session with role-based access
            user_role = UserRole(role)
            session.login_user(user_id, username, user_role)
            
            self.controller.login_user(user_id, username, user_role)
            self._clear_fields()
        else:
            self.status_label.config(text=message, foreground="red")
    
    def _continue_as_guest(self):
        # Handle guest login
        # Set up guest session
        guest_user = session.login_guest()
        
        self.status_label.config(text="Continuing as guest...", foreground="green")
        self.controller.login_user(None, "Guest", UserRole.GUEST)
        self._clear_fields()
    
    def _register(self):
        # Handle register button click
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="Please enter username and password")
            return
        
        success, message = register(username, password)
        if success:
            self.status_label.config(text=f"Account created! Please login.", foreground="green")
        else:
            self.status_label.config(text=message, foreground="red")
    
    def _clear_fields(self):
        # Clear input fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="")
    
    def on_show(self):
        # Called when frame is shown
        self._clear_fields()
        self.username_entry.focus()
