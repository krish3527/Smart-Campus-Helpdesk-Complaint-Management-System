"""
views/register_view.py - Screen 2: Student Registration for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_SIDEBAR,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StyledButton, load_app_logo, APP_NAME
)
from data_manager import DataManager

class RegisterView(tk.Frame):
    def __init__(self, parent, on_navigate_login, on_registration_success):
        super().__init__(parent, bg=COLOR_BG)
        self.on_navigate_login = on_navigate_login
        self.on_registration_success = on_registration_success
        self.dm = DataManager()

        self._build_ui()

    def _build_ui(self):
        # Outer scrollable container to ensure it fits nicely on any laptop screen
        canvas = tk.Canvas(self, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_BG)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Inner container centered
        inner_container = tk.Frame(scrollable_frame, bg=COLOR_BG, pady=24)
        inner_container.pack(anchor="center")

        card = tk.Frame(
            inner_container,
            bg=COLOR_CARD,
            padx=36,
            pady=26,
            highlightbackground=COLOR_BORDER,
            highlightcolor=COLOR_BORDER,
            highlightthickness=1,
            bd=0,
            width=520
        )
        card.pack()

        # Display UniResolve Logo maintaining proportions
        logo_photo = load_app_logo(max_width=70, max_height=70)
        if logo_photo:
            lbl_logo = tk.Label(card, image=logo_photo, bg=COLOR_CARD)
            lbl_logo.image = logo_photo
            lbl_logo.pack(pady=(0, 6))

        # Top Header
        lbl_head = tk.Label(
            card,
            text=f"{APP_NAME} Student Registration",
            font=(FONT_TITLE_LARGE[0], 15, "bold"),
            fg=COLOR_SIDEBAR,
            bg=COLOR_CARD
        )
        lbl_head.pack()

        lbl_sub = tk.Label(
            card,
            text="Register with your official SRMIST university credentials (* required)",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_sub.pack(pady=(2, 14))

        # Form fields layout (2-column grid for clean desktop application look)
        form_grid = tk.Frame(card, bg=COLOR_CARD)
        form_grid.pack(fill="x")
        form_grid.columnconfigure(0, weight=1, uniform="reg_col")
        form_grid.columnconfigure(1, weight=1, uniform="reg_col")

        # Helper to create input field with hint/placeholder
        def create_entry(parent, label_text, row, col, columnspan=1, placeholder=""):
            lbl = tk.Label(
                parent,
                text=label_text,
                font=FONT_SMALL_BOLD,
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD,
                anchor="w"
            )
            lbl.grid(row=row*2, column=col, columnspan=columnspan, sticky="w", padx=6, pady=(6, 2))

            ent = tk.Entry(
                parent,
                font=FONT_BODY,
                bg="#FAFCFB",
                fg=COLOR_TEXT_MAIN,
                relief="solid",
                bd=1,
                highlightthickness=0
            )
            ent.grid(row=row*2+1, column=col, columnspan=columnspan, sticky="ew", padx=6, pady=(0, 6), ipady=5)

            if placeholder:
                # Add placeholder styling
                ent.insert(0, placeholder)
                ent.config(fg="#9AA8A0")

                def on_focus_in(event, e=ent, p=placeholder):
                    if e.get() == p:
                        e.delete(0, tk.END)
                        e.config(fg=COLOR_TEXT_MAIN)

                def on_focus_out(event, e=ent, p=placeholder):
                    if not e.get():
                        e.insert(0, p)
                        e.config(fg="#9AA8A0")

                ent.bind("<FocusIn>", on_focus_in)
                ent.bind("<FocusOut>", on_focus_out)

            return ent

        # Row 0: Full Name (spans 2 columns)
        self.ent_name = create_entry(form_grid, "Full Legal Name *", 0, 0, columnspan=2)

        # Row 1: Registration Number & Department
        self.ent_reg = create_entry(
            form_grid,
            "Registration Number * (e.g. RA2511000000)",
            1, 0,
            placeholder="RA2511000000"
        )

        # Department Combobox
        lbl_dept = tk.Label(form_grid, text="Department *", font=FONT_SMALL_BOLD, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w")
        lbl_dept.grid(row=2, column=1, sticky="w", padx=6, pady=(6, 2))

        departments = [
            "Computer Science & Engineering",
            "Information Technology",
            "Electronics & Communication",
            "Electrical & Electronics",
            "Mechanical Engineering",
            "Civil Engineering",
            "Biotechnology",
            "Data Science & AI"
        ]
        self.cb_dept = ttk.Combobox(form_grid, values=departments, state="readonly", font=FONT_BODY)
        self.cb_dept.set(departments[0])
        self.cb_dept.grid(row=3, column=1, sticky="ew", padx=6, pady=(0, 6), ipady=3)

        # Row 2: Year of Study & Email
        lbl_year = tk.Label(form_grid, text="Year of Study *", font=FONT_SMALL_BOLD, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w")
        lbl_year.grid(row=4, column=0, sticky="w", padx=6, pady=(6, 2))

        years = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Postgraduate"]
        self.cb_year = ttk.Combobox(form_grid, values=years, state="readonly", font=FONT_BODY)
        self.cb_year.set(years[0])
        self.cb_year.grid(row=5, column=0, sticky="ew", padx=6, pady=(0, 6), ipady=3)

        self.ent_email = create_entry(
            form_grid,
            "SRMIST Email * (@srmist.edu.in)",
            2, 1,
            placeholder="student@srmist.edu.in"
        )

        # Row 3: Username & Password
        self.ent_user = create_entry(form_grid, "Portal Username *", 3, 0)

        lbl_pwd = tk.Label(form_grid, text="Account Password *", font=FONT_SMALL_BOLD, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w")
        lbl_pwd.grid(row=6, column=1, sticky="w", padx=6, pady=(6, 2))

        self.ent_pwd = tk.Entry(
            form_grid,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            show="*",
            highlightthickness=0
        )
        self.ent_pwd.grid(row=7, column=1, sticky="ew", padx=6, pady=(0, 6), ipady=5)

        # Action Buttons
        btn_frame = tk.Frame(card, bg=COLOR_CARD)
        btn_frame.pack(fill="x", pady=(18, 8))

        btn_register = StyledButton(
            btn_frame,
            text="Complete UniResolve Registration",
            style_type="primary",
            command=self._on_register
        )
        btn_register.pack(fill="x", ipady=4, pady=(0, 8))

        btn_clear = StyledButton(
            btn_frame,
            text="Clear Form",
            style_type="secondary",
            command=self._clear_form
        )
        btn_clear.pack(fill="x", ipady=2, pady=(0, 12))

        # Back to Login
        back_row = tk.Frame(card, bg=COLOR_CARD)
        back_row.pack(fill="x")

        lbl_already = tk.Label(
            back_row,
            text="Already have an account?",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_already.pack(side="left")

        btn_back = tk.Button(
            back_row,
            text="Back to Sign In",
            command=self.on_navigate_login,
            font=FONT_SMALL_BOLD,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD,
            activeforeground="#1E7548",
            activebackground=COLOR_CARD,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn_back.pack(side="left", padx=5)

    def _get_val(self, entry, placeholder=""):
        val = entry.get().strip()
        if val == placeholder:
            return ""
        return val

    def _clear_form(self):
        self.ent_name.delete(0, tk.END)
        self.ent_reg.delete(0, tk.END)
        self.ent_reg.insert(0, "RA2511000000")
        self.ent_reg.config(fg="#9AA8A0")

        self.ent_email.delete(0, tk.END)
        self.ent_email.insert(0, "student@srmist.edu.in")
        self.ent_email.config(fg="#9AA8A0")

        self.ent_user.delete(0, tk.END)
        self.ent_pwd.delete(0, tk.END)
        self.cb_dept.current(0)
        self.cb_year.current(0)

    def _on_register(self):
        name = self._get_val(self.ent_name)
        reg_no = self._get_val(self.ent_reg, "RA2511000000")
        dept = self.cb_dept.get()
        year = self.cb_year.get()
        email = self._get_val(self.ent_email, "student@srmist.edu.in")
        username = self._get_val(self.ent_user)
        password = self.ent_pwd.get().strip()

        success, msg = self.dm.register_student(
            name, reg_no, dept, year, email, username, password
        )

        if success:
            messagebox.showinfo("Registration Successful", msg, parent=self)
            self.on_registration_success(username.strip().lower())
        else:
            messagebox.showerror("Registration Validation Error", msg, parent=self)
