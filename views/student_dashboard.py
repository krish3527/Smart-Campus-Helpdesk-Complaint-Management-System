"""
views/student_dashboard.py - Screen 3: Student Dashboard for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_PENDING, COLOR_IN_PROGRESS, COLOR_RESOLVED,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StatCard, StyledButton, APP_NAME
)
from data_manager import DataManager
from views.details_dialog import ComplaintDetailsDialog

class StudentDashboardView(tk.Frame):
    def __init__(self, parent, user_data, on_navigate):
        super().__init__(parent, bg=COLOR_BG)
        self.user_data = user_data
        self.on_navigate = on_navigate
        self.dm = DataManager()

        self._build_ui()
        self.refresh_dashboard()

    def _build_ui(self):
        # 1. Top Bar
        now_str = datetime.now().strftime("%A, %d %B %Y")
        top = tk.Frame(self, bg=COLOR_BG, padx=28, pady=20)
        top.pack(fill="x")

        # Top row: Welcome message + Quick action button
        welcome_row = tk.Frame(top, bg=COLOR_BG)
        welcome_row.pack(fill="x")

        user_name = self.user_data.get("name", "Student")
        lbl_welcome = tk.Label(
            welcome_row,
            text=f"Welcome back, {user_name} 👋",
            font=FONT_TITLE_LARGE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_welcome.pack(side="left")

        btn_new_complaint = StyledButton(
            welcome_row,
            text="➕ Submit New Complaint",
            style_type="primary",
            command=lambda: self.on_navigate("submit_complaint")
        )
        btn_new_complaint.pack(side="right")

        # Subtitle with student metadata
        dept = self.user_data.get("department", "Student")
        reg_no = self.user_data.get("reg_no", "")
        lbl_sub = tk.Label(
            top,
            text=f"Registration No: {reg_no}   •   Dept: {dept}   •   {now_str}",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_sub.pack(fill="x", pady=(4, 0))

        # 2. Statistics Grid
        stats_frame = tk.Frame(self, bg=COLOR_BG, padx=28)
        stats_frame.pack(fill="x", pady=(0, 16))

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        stats_frame.columnconfigure(3, weight=1)

        self.card_total = StatCard(stats_frame, "Total Complaints", "0", accent_color=COLOR_PRIMARY, subtitle="Submitted by you")
        self.card_total.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.card_pending = StatCard(stats_frame, "Pending", "0", accent_color=COLOR_PENDING, subtitle="Awaiting facility review")
        self.card_pending.grid(row=0, column=1, sticky="nsew", padx=4)

        self.card_progress = StatCard(stats_frame, "In Progress", "0", accent_color=COLOR_IN_PROGRESS, subtitle="Technician assigned")
        self.card_progress.grid(row=0, column=2, sticky="nsew", padx=4)

        self.card_resolved = StatCard(stats_frame, "Resolved", "0", accent_color=COLOR_RESOLVED, subtitle="Successfully closed")
        self.card_resolved.grid(row=0, column=3, sticky="nsew", padx=(8, 0))

        # 3. Main Content Card: Recent Complaints
        content_frame = tk.Frame(self, bg=COLOR_BG, padx=28, pady=4)
        content_frame.pack(fill="both", expand=True)

        card = tk.Frame(
            content_frame,
            bg=COLOR_CARD,
            padx=20,
            pady=16,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        card.pack(fill="both", expand=True)

        # Card Header
        card_header = tk.Frame(card, bg=COLOR_CARD)
        card_header.pack(fill="x", pady=(0, 12))

        lbl_table_title = tk.Label(
            card_header,
            text="Recent Campus Complaints",
            font=FONT_TITLE_MED,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_table_title.pack(side="left")

        lbl_table_hint = tk.Label(
            card_header,
            text="(Double click any complaint to view full record)",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_table_hint.pack(side="left", padx=8)

        btn_view_all = StyledButton(
            card_header,
            text="View All My Complaints ➔",
            style_type="outline",
            command=lambda: self.on_navigate("my_complaints")
        )
        btn_view_all.pack(side="right")

        # Table container
        table_container = tk.Frame(card, bg=COLOR_CARD)
        table_container.pack(fill="both", expand=True)

        columns = ("id", "title", "category", "location", "date", "status")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="Complaint ID", anchor="center")
        self.tree.heading("title", text="Complaint Title", anchor="w")
        self.tree.heading("category", text="Category", anchor="w")
        self.tree.heading("location", text="Location", anchor="w")
        self.tree.heading("date", text="Date Filed", anchor="center")
        self.tree.heading("status", text="Current Status", anchor="center")

        self.tree.column("id", width=110, minwidth=90, anchor="center")
        self.tree.column("title", width=300, minwidth=200, anchor="w")
        self.tree.column("category", width=170, minwidth=130, anchor="w")
        self.tree.column("location", width=140, minwidth=110, anchor="w")
        self.tree.column("date", width=110, minwidth=90, anchor="center")
        self.tree.column("status", width=130, minwidth=100, anchor="center")

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Double click to view details
        self.tree.bind("<Double-1>", self._on_double_click_row)

        # Bottom buttons row inside card
        btn_bar = tk.Frame(card, bg=COLOR_CARD)
        btn_bar.pack(fill="x", pady=(12, 0))

        btn_details = StyledButton(
            btn_bar,
            text="🔍 View Complaint Details",
            style_type="secondary",
            command=self._view_selected_details
        )
        btn_details.pack(side="left", padx=(0, 8))

        btn_refresh = StyledButton(
            btn_bar,
            text="🔄 Refresh",
            style_type="outline",
            command=self.refresh_dashboard
        )
        btn_refresh.pack(side="left")

    def refresh_dashboard(self):
        """Reload statistics and recent complaints table."""
        username = self.user_data.get("username", "")

        # 1. Update Stat Cards
        stats = self.dm.get_stats_for_student(username)
        self.card_total.update_value(stats["total"])
        self.card_pending.update_value(stats["pending"])
        self.card_progress.update_value(stats["in_progress"])
        self.card_resolved.update_value(stats["resolved"])

        # 2. Update Recent Complaints Table
        for row in self.tree.get_children():
            self.tree.delete(row)

        complaints = self.dm.get_complaints_by_student(username)

        for i, c in enumerate(complaints[:10]):
            status_text = c.get("status", "Pending")
            tag_name = f"row_{c['id']}"

            self.tree.insert(
                "",
                "end",
                values=(
                    c.get("id"),
                    c.get("title"),
                    c.get("category"),
                    c.get("location"),
                    c.get("date"),
                    f"● {status_text}"
                ),
                tags=(tag_name, "even" if i % 2 == 0 else "odd")
            )

            if status_text == "Pending":
                self.tree.tag_configure(tag_name, foreground=COLOR_PENDING)
            elif status_text == "In Progress":
                self.tree.tag_configure(tag_name, foreground=COLOR_IN_PROGRESS)
            elif status_text == "Resolved":
                self.tree.tag_configure(tag_name, foreground=COLOR_RESOLVED)

    def _on_double_click_row(self, event):
        self._view_selected_details()

    def _view_selected_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Selection Required",
                "Please select a complaint from the table to view its details.",
                parent=self
            )
            return

        item = self.tree.item(selected[0])
        cid = item["values"][0]
        ComplaintDetailsDialog(
            self.winfo_toplevel(),
            complaint_id=cid,
            is_admin=False,
            on_update_callback=self.refresh_dashboard
        )
