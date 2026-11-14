"""
views/login_view.py - Screen 1: Login Page for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_SIDEBAR,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StyledButton, load_app_logo, APP_NAME, APP_TAGLINE
)
from data_manager import DataManager
from views.forgot_password_dialog import ForgotPasswordDialog

class LoginView(tk.Frame):
    def __init__(self, parent, on_login_success, on_navigate_register):
        super().__init__(parent, bg=COLOR_BG)
        self.on_login_success = on_login_success
        self.on_navigate_register = on_navigate_register
        self.dm = DataManager()

        self._build_ui()

    def _build_ui(self):
        # Outer wrapper centered
        wrapper = tk.Frame(self, bg=COLOR_BG)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        # Login Card Container
        card = tk.Frame(
            wrapper,
            bg=COLOR_CARD,
            padx=38,
            pady=30,
            highlightbackground=COLOR_BORDER,
            highlightcolor=COLOR_BORDER,
            highlightthickness=1,
            bd=0,
            width=460
        )
        card.pack()

        # Logo / Emblem maintaining original proportions
        logo_photo = load_app_logo(max_width=80, max_height=80)
        if logo_photo:
            lbl_logo = tk.Label(card, image=logo_photo, bg=COLOR_CARD)
            lbl_logo.image = logo_photo
            lbl_logo.pack(pady=(0, 8))

        # Title & Subtitle / Tagline
        lbl_title = tk.Label(
            card,
            text=APP_NAME,
            font=(FONT_TITLE_LARGE[0], 18, "bold"),
            fg=COLOR_SIDEBAR,
            bg=COLOR_CARD
        )
        lbl_title.pack()

        lbl_tagline = tk.Label(
            card,
            text=APP_TAGLINE,
            font=(FONT_SMALL[0], 9, "italic"),
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD
        )
        lbl_tagline.pack(pady=(2, 14))

        # Role Selection (Student vs Administrator)
        lbl_role = tk.Label(
            card,
            text="Select Portal Role:",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_role.pack(fill="x", pady=(0, 4))

        self.role_var = tk.StringVar(value="student")
        role_frame = tk.Frame(card, bg=COLOR_CARD)
        role_frame.pack(fill="x", pady=(0, 12))

        rb_student = tk.Radiobutton(
            role_frame,
            text="Student",
            variable=self.role_var,
            value="student",
            font=FONT_BODY_BOLD,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_CARD,
            selectcolor="#E9EFEA",
            cursor="hand2"
        )
        rb_student.pack(side="left", padx=(0, 24))

        rb_admin = tk.Radiobutton(
            role_frame,
            text="Administrator",
            variable=self.role_var,
            value="admin",
            font=FONT_BODY_BOLD,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_CARD,
            selectcolor="#E9EFEA",
            cursor="hand2"
        )
        rb_admin.pack(side="left")

        # Username Input
        lbl_user = tk.Label(
            card,
            text="Username",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_user.pack(fill="x", pady=(0, 3))

        self.ent_user = tk.Entry(
            card,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=0,
            width=34
        )
        self.ent_user.pack(fill="x", ipady=6, pady=(0, 10))

        # Password Input Header Row (with Forgot Password link)
        pwd_header = tk.Frame(card, bg=COLOR_CARD)
        pwd_header.pack(fill="x", pady=(0, 3))

        lbl_pwd = tk.Label(
            pwd_header,
            text="Password",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_pwd.pack(side="left")

        btn_forgot = tk.Button(
            pwd_header,
            text="Forgot Password?",
            command=self._open_forgot_password,
            font=FONT_SMALL,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD,
            activeforeground=COLOR_PRIMARY_HOVER,
            activebackground=COLOR_CARD,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn_forgot.pack(side="right")

        self.ent_pwd = tk.Entry(
            card,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            show="*",
            highlightthickness=0,
            width=34
        )
        self.ent_pwd.pack(fill="x", ipady=6, pady=(0, 6))

        # Show password toggle
        self.show_pwd_var = tk.BooleanVar(value=False)
        chk_show = tk.Checkbutton(
            card,
            text="Show password",
            variable=self.show_pwd_var,
            command=self._toggle_pwd,
            font=FONT_SMALL,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_CARD,
            bd=0,
            cursor="hand2"
        )
        chk_show.pack(anchor="w", pady=(0, 14))

        # Enter key triggers login
        self.ent_user.bind("<Return>", lambda e: self._on_login())
        self.ent_pwd.bind("<Return>", lambda e: self._on_login())

        # Prominent Login Button
        btn_login = StyledButton(
            card,
            text="Sign In to UniResolve",
            style_type="primary",
            command=self._on_login
        )
        btn_login.pack(fill="x", ipady=4, pady=(0, 14))

        # Register Option
        reg_row = tk.Frame(card, bg=COLOR_CARD)
        reg_row.pack(fill="x")

        lbl_no_acc = tk.Label(
            reg_row,
            text="New SRMIST student?",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_no_acc.pack(side="left")

        btn_reg = tk.Button(
            reg_row,
            text="Register Here",
            command=self.on_navigate_register,
            font=FONT_SMALL_BOLD,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD,
            activeforeground=COLOR_PRIMARY_HOVER,
            activebackground=COLOR_CARD,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn_reg.pack(side="left", padx=5)

        # Demo Credentials Box for Easy Viva Evaluation
        demo_box = tk.Frame(
            card,
            bg="#F0F5F2",
            padx=12,
            pady=10,
            highlightbackground="#D5E2D9",
            highlightthickness=1,
            bd=0
        )
        demo_box.pack(fill="x", pady=(18, 0))

        lbl_demo_title = tk.Label(
            demo_box,
            text="⚡ QUICK DEMO CREDENTIALS (CLICK TO AUTO-FILL)",
            font=(FONT_SMALL_BOLD[0], 8, "bold"),
            fg=COLOR_SIDEBAR,
            bg="#F0F5F2"
        )
        lbl_demo_title.pack(anchor="w", pady=(0, 6))

        demo_btns = tk.Frame(demo_box, bg="#F0F5F2")
        demo_btns.pack(fill="x")

        btn_fill_stu = tk.Button(
            demo_btns,
            text="Student (student1)",
            font=FONT_SMALL,
            bg="#FFFFFF",
            fg=COLOR_TEXT_MAIN,
            activebackground="#E2ECE5",
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=8,
            pady=3,
            command=self._fill_demo_student
        )
        btn_fill_stu.pack(side="left", padx=(0, 8))

        btn_fill_admin = tk.Button(
            demo_btns,
            text="Admin (admin)",
            font=FONT_SMALL,
            bg="#FFFFFF",
            fg=COLOR_TEXT_MAIN,
            activebackground="#E2ECE5",
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=8,
            pady=3,
            command=self._fill_demo_admin
        )
        btn_fill_admin.pack(side="left")

    def _toggle_pwd(self):
        if self.show_pwd_var.get():
            self.ent_pwd.config(show="")
        else:
            self.ent_pwd.config(show="*")

    def _open_forgot_password(self):
        ForgotPasswordDialog(
            self.winfo_toplevel(),
            on_recovery_success=self.prefill_username
        )

    def _fill_demo_student(self):
        self.role_var.set("student")
        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, "student1")
        self.ent_pwd.delete(0, tk.END)
        self.ent_pwd.insert(0, "student123")

    def _fill_demo_admin(self):
        self.role_var.set("admin")
        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, "admin")
        self.ent_pwd.delete(0, tk.END)
        self.ent_pwd.insert(0, "admin123")

    def _on_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pwd.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror(
                "Login Error",
                "Please enter both username and password.",
                parent=self
            )
            return

        user = self.dm.authenticate(username, password, role)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror(
                "Authentication Failed",
                f"Invalid credentials for {role.capitalize()} role.\n\nPlease check your username and password or select the correct role.",
                parent=self
            )

    def prefill_username(self, username):
        """Called after successful registration or password reset."""
        self.role_var.set("student")
        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, username)
        self.ent_pwd.delete(0, tk.END)
        self.ent_pwd.focus_set()
