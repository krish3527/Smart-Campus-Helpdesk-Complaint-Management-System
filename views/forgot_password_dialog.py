"""
views/forgot_password_dialog.py - Screen: Forgot Password / Student Recovery
UniResolve - Campus Helpdesk & Complaint Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_SIDEBAR,
    FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StyledButton, load_app_logo, APP_NAME
)
from data_manager import DataManager

class ForgotPasswordDialog(tk.Toplevel):
    def __init__(self, parent, on_recovery_success):
        super().__init__(parent)
        self.on_recovery_success = on_recovery_success
        self.dm = DataManager()
        self.verified_student = None

        self.title(f"{APP_NAME} - Student Password Recovery")
        self.geometry("480x560")
        self.minsize(440, 500)
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._center_window(parent)
        self._build_ui()

    def _center_window(self, parent):
        self.update_idletasks()
        try:
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            w = 480
            h = 560
            x = px + (pw - w) // 2
            y = py + (ph - h) // 2
            self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

    def _build_ui(self):
        container = tk.Frame(self, bg=COLOR_BG, padx=24, pady=20)
        container.pack(fill="both", expand=True)

        card = tk.Frame(
            container,
            bg=COLOR_CARD,
            padx=26,
            pady=22,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        card.pack(fill="both", expand=True)

        # Header with Logo
        logo_photo = load_app_logo(max_width=50, max_height=50)
        if logo_photo:
            lbl_logo = tk.Label(card, image=logo_photo, bg=COLOR_CARD)
            lbl_logo.image = logo_photo
            lbl_logo.pack(pady=(0, 6))

        lbl_head = tk.Label(
            card,
            text="Student Password Recovery",
            font=FONT_TITLE_MED,
            fg=COLOR_SIDEBAR,
            bg=COLOR_CARD
        )
        lbl_head.pack()

        lbl_sub = tk.Label(
            card,
            text="Verify your registered university details to set a new password",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD,
            wraplength=380
        )
        lbl_sub.pack(pady=(2, 14))

        # --- STEP 1: Verification Section ---
        self.step1_frame = tk.Frame(card, bg=COLOR_CARD)
        self.step1_frame.pack(fill="x")

        lbl_email = tk.Label(
            self.step1_frame,
            text="Registered SRMIST Email *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_email.pack(fill="x", pady=(0, 2))

        self.ent_email = tk.Entry(
            self.step1_frame,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        self.ent_email.pack(fill="x", ipady=5, pady=(0, 10))

        lbl_reg = tk.Label(
            self.step1_frame,
            text="Registration Number * (e.g. RA2511000000)",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_reg.pack(fill="x", pady=(0, 2))

        self.ent_reg = tk.Entry(
            self.step1_frame,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        self.ent_reg.pack(fill="x", ipady=5, pady=(0, 14))

        self.btn_verify = StyledButton(
            self.step1_frame,
            text="🔍 Verify Credentials",
            style_type="primary",
            command=self._on_verify_details
        )
        self.btn_verify.pack(fill="x", ipady=2)

        # Verification Status Badge
        self.lbl_verify_status = tk.Label(
            card,
            text="",
            font=FONT_SMALL_BOLD,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD,
            wraplength=380
        )
        self.lbl_verify_status.pack(pady=(10, 4))

        # --- STEP 2: Password Reset Section (Revealed upon verification) ---
        self.step2_frame = tk.Frame(card, bg=COLOR_CARD)

        lbl_new_pwd = tk.Label(
            self.step2_frame,
            text="New Password *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_new_pwd.pack(fill="x", pady=(0, 2))

        self.ent_new_pwd = tk.Entry(
            self.step2_frame,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            show="*",
            highlightthickness=0
        )
        self.ent_new_pwd.pack(fill="x", ipady=5, pady=(0, 8))

        lbl_conf_pwd = tk.Label(
            self.step2_frame,
            text="Confirm New Password *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_conf_pwd.pack(fill="x", pady=(0, 2))

        self.ent_conf_pwd = tk.Entry(
            self.step2_frame,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            show="*",
            highlightthickness=0
        )
        self.ent_conf_pwd.pack(fill="x", ipady=5, pady=(0, 6))

        # Show password toggle
        self.show_pwd_var = tk.BooleanVar(value=False)
        chk_show = tk.Checkbutton(
            self.step2_frame,
            text="Show passwords",
            variable=self.show_pwd_var,
            command=self._toggle_passwords,
            font=FONT_SMALL,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_CARD,
            bd=0,
            cursor="hand2"
        )
        chk_show.pack(anchor="w", pady=(0, 10))

        btn_save = StyledButton(
            self.step2_frame,
            text="💾 Update Password",
            style_type="primary",
            command=self._on_save_password
        )
        btn_save.pack(fill="x", ipady=2)

        # Cancel / Close
        btn_cancel = StyledButton(
            card,
            text="Cancel & Return to Login",
            style_type="outline",
            command=self.destroy
        )
        btn_cancel.pack(side="bottom", fill="x", pady=(10, 0))

    def _toggle_passwords(self):
        char = "" if self.show_pwd_var.get() else "*"
        self.ent_new_pwd.config(show=char)
        self.ent_conf_pwd.config(show=char)

    def _on_verify_details(self):
        email = self.ent_email.get().strip()
        reg_no = self.ent_reg.get().strip()

        if not email or not reg_no:
            messagebox.showerror(
                "Input Required",
                "Please enter both your registered SRMIST Email and Registration Number.",
                parent=self
            )
            return

        # Email domain validation
        is_valid_email, err = self.dm.validate_srmist_email(email)
        if not is_valid_email:
            messagebox.showerror("Invalid Email", err, parent=self)
            return

        # Registration Number format validation
        is_valid_reg, reg_err = self.dm.validate_srmist_reg_no(reg_no)
        if not is_valid_reg:
            messagebox.showerror("Invalid Registration Number", reg_err, parent=self)
            return

        student = self.dm.verify_student_for_recovery(email, reg_no)
        if student:
            self.verified_student = student
            self.ent_email.config(state="disabled")
            self.ent_reg.config(state="disabled")
            self.btn_verify.config(state="disabled")

            self.lbl_verify_status.config(
                text=f"✓ Verified: {student['name']} ({student['username']})\nPlease enter your new password below.",
                fg=COLOR_PRIMARY
            )
            self.step2_frame.pack(fill="x", pady=(6, 0))
            self.ent_new_pwd.focus_set()
        else:
            messagebox.showerror(
                "Verification Failed",
                "No registered student found matching this Email and Registration Number.\nPlease check your details and try again.",
                parent=self
            )

    def _on_save_password(self):
        if not self.verified_student:
            return

        new_p = self.ent_new_pwd.get().strip()
        conf_p = self.ent_conf_pwd.get().strip()

        if not new_p or not conf_p:
            messagebox.showerror(
                "Password Required",
                "Please enter and confirm your new password.",
                parent=self
            )
            return

        if len(new_p) < 4:
            messagebox.showerror(
                "Password Too Short",
                "Password must be at least 4 characters long.",
                parent=self
            )
            return

        if new_p != conf_p:
            messagebox.showerror(
                "Passwords Do Not Match",
                "The entered passwords do not match. Please re-enter them carefully.",
                parent=self
            )
            return

        username = self.verified_student["username"]
        success, msg = self.dm.reset_password(username, new_p)

        if success:
            messagebox.showinfo(
                "Password Reset Successful",
                f"Password for user '{username}' has been successfully reset!\nYou can now log in with your new password.",
                parent=self
            )
            self.destroy()
            if self.on_recovery_success:
                self.on_recovery_success(username)
        else:
            messagebox.showerror("Error", msg, parent=self)
