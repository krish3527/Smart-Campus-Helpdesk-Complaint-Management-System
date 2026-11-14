"""
main.py - UniResolve: Campus Helpdesk & Complaint Management System
Your Campus. Your Voice. Our Resolution.
College-level Python Tkinter Desktop Application
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Enable High-DPI awareness on Windows for crisp rendering
if sys.platform.startswith("win"):
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

from ui_components import (
    COLOR_BG, COLOR_SIDEBAR, setup_app_styles, Sidebar, load_app_logo, APP_NAME, APP_TAGLINE
)
from data_manager import DataManager
from views.login_view import LoginView
from views.register_view import RegisterView
from views.student_dashboard import StudentDashboardView
from views.submit_complaint import SubmitComplaintView
from views.my_complaints import MyComplaintsView
from views.admin_dashboard import AdminDashboardView
from views.admin_manage import AdminManageView
from views.help_view import HelpView

class UniResolveApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} - Campus Helpdesk & Complaint Management System")
        self.geometry("1180x750")
        self.minsize(980, 620)
        self.configure(bg=COLOR_BG)

        # Center on screen
        self._center_window()

        # Application Icon
        self._set_app_icon()

        # Setup ttk styles
        setup_app_styles()

        # Shared Data Store
        self.dm = DataManager()
        self.current_user = None
        self.current_screen_name = None

        # Container frames
        self.main_container = tk.Frame(self, bg=COLOR_BG)
        self.main_container.pack(fill="both", expand=True)

        # Active view tracking
        self.sidebar = None
        self.content_frame = None

        # Start with Login Page
        self.show_login()

    def _center_window(self):
        self.update_idletasks()
        try:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            win_w = 1180
            win_h = 750
            x = (screen_w - win_w) // 2
            y = (screen_h - win_h) // 2 - 20
            self.geometry(f"{win_w}x{win_h}+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

    def _set_app_icon(self):
        icon_photo = load_app_logo(max_width=64, max_height=64)
        if icon_photo:
            try:
                self.icon_photo = icon_photo
                self.iconphoto(False, self.icon_photo)
            except Exception:
                pass

    def _clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        self.sidebar = None
        self.content_frame = None

    # --- Screen Switching Logic ---

    def show_login(self, prefill_username=None):
        self.current_user = None
        self._clear_main_container()

        login_view = LoginView(
            parent=self.main_container,
            on_login_success=self.on_login_success,
            on_navigate_register=self.show_register
        )
        login_view.pack(fill="both", expand=True)

        if prefill_username:
            login_view.prefill_username(prefill_username)

    def show_register(self):
        self._clear_main_container()

        reg_view = RegisterView(
            parent=self.main_container,
            on_navigate_login=self.show_login,
            on_registration_success=lambda u: self.show_login(prefill_username=u)
        )
        reg_view.pack(fill="both", expand=True)

    def on_login_success(self, user):
        self.current_user = user
        self.setup_authenticated_layout()

    def setup_authenticated_layout(self):
        """Construct the two-panel interface: Left Sidebar + Right Content Area."""
        self._clear_main_container()

        is_admin = (self.current_user.get("role") == "admin")

        if is_admin:
            nav_items = [
                ("dashboard", "📊  Dashboard"),
                ("manage_complaints", "⚙️  All Complaints"),
                ("help", "❓  Help & FAQ")
            ]
            default_screen = "dashboard"
        else:
            nav_items = [
                ("dashboard", "📊  Dashboard"),
                ("submit_complaint", "📝  Submit Complaint"),
                ("my_complaints", "📋  My Complaints"),
                ("help", "❓  Help & FAQ")
            ]
            default_screen = "dashboard"

        # Sidebar Panel
        self.sidebar = Sidebar(
            parent=self.main_container,
            user_data=self.current_user,
            nav_items=nav_items,
            active_nav=default_screen,
            on_nav_select=self.navigate_to_screen,
            on_logout=self.show_login
        )
        self.sidebar.pack(side="left", fill="y")

        # Right Content Panel
        self.content_frame = tk.Frame(self.main_container, bg=COLOR_BG)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Show initial screen
        self.navigate_to_screen(default_screen)

    def navigate_to_screen(self, screen_key):
        """Switch the view rendered in the right content panel."""
        if not self.content_frame:
            return

        for w in self.content_frame.winfo_children():
            w.destroy()

        self.current_screen_name = screen_key

        # Update active state in sidebar buttons
        if self.sidebar and hasattr(self.sidebar, "nav_buttons"):
            for key, btn in self.sidebar.nav_buttons.items():
                if key == screen_key:
                    btn.config(bg="#238653", fg="#FFFFFF", font=("Segoe UI", 10, "bold"))
                else:
                    btn.config(bg=COLOR_SIDEBAR, fg="#C4D6CC", font=("Segoe UI", 10))

        role = self.current_user.get("role")

        if role == "student":
            if screen_key == "dashboard":
                view = StudentDashboardView(self.content_frame, self.current_user, self.navigate_to_screen)
            elif screen_key == "submit_complaint":
                view = SubmitComplaintView(self.content_frame, self.current_user, self.navigate_to_screen)
            elif screen_key == "my_complaints":
                view = MyComplaintsView(self.content_frame, self.current_user, self.navigate_to_screen)
            elif screen_key == "help":
                view = HelpView(self.content_frame, self.current_user)
            else:
                view = StudentDashboardView(self.content_frame, self.current_user, self.navigate_to_screen)

        elif role == "admin":
            if screen_key == "dashboard":
                view = AdminDashboardView(self.content_frame, self.current_user, self.navigate_to_screen)
            elif screen_key == "manage_complaints":
                view = AdminManageView(self.content_frame, self.current_user, self.navigate_to_screen)
            elif screen_key == "help":
                view = HelpView(self.content_frame, self.current_user)
            else:
                view = AdminDashboardView(self.content_frame, self.current_user, self.navigate_to_screen)
        else:
            view = tk.Label(self.content_frame, text="Unknown role", bg=COLOR_BG)

        view.pack(fill="both", expand=True)

# Compatibility alias
SmartCampusApp = UniResolveApp

if __name__ == "__main__":
    app = UniResolveApp()
    app.mainloop()
