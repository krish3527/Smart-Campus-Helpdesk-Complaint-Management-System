"""
views/admin_dashboard.py - Screen 6: Administrator Dashboard for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_PENDING, COLOR_IN_PROGRESS, COLOR_RESOLVED, COLOR_DANGER,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StatCard, StyledButton, APP_NAME
)
from data_manager import DataManager
from views.details_dialog import ComplaintDetailsDialog

class AdminDashboardView(tk.Frame):
    def __init__(self, parent, user_data, on_navigate):
        super().__init__(parent, bg=COLOR_BG)
        self.user_data = user_data
        self.on_navigate = on_navigate
        self.dm = DataManager()

        self._build_ui()
        self.refresh_dashboard()

    def _build_ui(self):
        # 1. Top Header Bar
        now_str = datetime.now().strftime("%A, %d %B %Y")
        top = tk.Frame(self, bg=COLOR_BG, padx=28, pady=20)
        top.pack(fill="x")

        head_row = tk.Frame(top, bg=COLOR_BG)
        head_row.pack(fill="x")

        lbl_welcome = tk.Label(
            head_row,
            text=f"{APP_NAME} - Administrator Console",
            font=FONT_TITLE_LARGE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_welcome.pack(side="left")

        btn_manage = StyledButton(
            head_row,
            text="⚙️ Manage All Campus Complaints",
            style_type="primary",
            command=lambda: self.on_navigate("manage_complaints")
        )
        btn_manage.pack(side="right")

        lbl_sub = tk.Label(
            top,
            text=f"SRMIST Campus Facility & Helpdesk Operations   •   System Date: {now_str}",
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

        self.card_total = StatCard(stats_frame, "Total Complaints", "0", accent_color=COLOR_PRIMARY, subtitle="Across entire campus")
        self.card_total.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.card_pending = StatCard(stats_frame, "Pending Attention", "0", accent_color=COLOR_PENDING, subtitle="Needs assignment")
        self.card_pending.grid(row=0, column=1, sticky="nsew", padx=4)

        self.card_progress = StatCard(stats_frame, "In Progress", "0", accent_color=COLOR_IN_PROGRESS, subtitle="Work in resolution")
        self.card_progress.grid(row=0, column=2, sticky="nsew", padx=4)

        self.card_resolved = StatCard(stats_frame, "Resolved", "0", accent_color=COLOR_RESOLVED, subtitle="Successfully closed")
        self.card_resolved.grid(row=0, column=3, sticky="nsew", padx=(8, 0))

        # 3. Middle Section: Split into Categories Summary (Left) and Recent Complaints Table (Right)
        mid_frame = tk.Frame(self, bg=COLOR_BG, padx=28, pady=4)
        mid_frame.pack(fill="both", expand=True)

        # Left Card: Category Breakdown
        cat_card = tk.Frame(
            mid_frame,
            bg=COLOR_CARD,
            padx=18,
            pady=16,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0,
            width=290
        )
        cat_card.pack(side="left", fill="y", padx=(0, 14))
        cat_card.pack_propagate(False)

        lbl_cat_head = tk.Label(
            cat_card,
            text="Complaints by Category",
            font=FONT_TITLE_MED,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_cat_head.pack(fill="x", pady=(0, 12))

        self.cat_list_frame = tk.Frame(cat_card, bg=COLOR_CARD)
        self.cat_list_frame.pack(fill="both", expand=True)

        # Right Card: Recent Complaints Table
        table_card = tk.Frame(
            mid_frame,
            bg=COLOR_CARD,
            padx=18,
            pady=16,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        table_card.pack(side="left", fill="both", expand=True)

        card_header = tk.Frame(table_card, bg=COLOR_CARD)
        card_header.pack(fill="x", pady=(0, 10))

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
            text="(Double click to inspect or update status)",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_table_hint.pack(side="left", padx=8)

        # Table
        columns = ("id", "student", "title", "location", "priority", "status")
        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID", anchor="center")
        self.tree.heading("student", text="Student Name", anchor="w")
        self.tree.heading("title", text="Title", anchor="w")
        self.tree.heading("location", text="Location", anchor="w")
        self.tree.heading("priority", text="Priority", anchor="center")
        self.tree.heading("status", text="Status", anchor="center")

        self.tree.column("id", width=80, minwidth=70, anchor="center")
        self.tree.column("student", width=130, minwidth=100, anchor="w")
        self.tree.column("title", width=220, minwidth=160, anchor="w")
        self.tree.column("location", width=130, minwidth=100, anchor="w")
        self.tree.column("priority", width=85, minwidth=70, anchor="center")
        self.tree.column("status", width=110, minwidth=90, anchor="center")

        tree_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._on_select_complaint())

        # Bottom Actions Bar
        bottom_bar = tk.Frame(self, bg=COLOR_BG, padx=28, pady=12)
        bottom_bar.pack(fill="x")

        btn_inspect = StyledButton(
            bottom_bar,
            text="🔍 Inspect / Update Selected",
            style_type="primary",
            command=self._on_select_complaint
        )
        btn_inspect.pack(side="left", padx=(0, 10))

        btn_refresh = StyledButton(
            bottom_bar,
            text="🔄 Refresh Dashboard",
            style_type="secondary",
            command=self.refresh_dashboard
        )
        btn_refresh.pack(side="left")

    def refresh_dashboard(self):
        """Update statistics, category cards, and table."""
        stats = self.dm.get_stats_for_admin()

        self.card_total.update_value(stats["total"])
        self.card_pending.update_value(stats["pending"])
        self.card_progress.update_value(stats["in_progress"])
        self.card_resolved.update_value(stats["resolved"])

        # Render Category Breakdown
        for w in self.cat_list_frame.winfo_children():
            w.destroy()

        categories = stats["categories"]
        for cat_name, count in categories.items():
            row = tk.Frame(self.cat_list_frame, bg=COLOR_CARD, pady=4)
            row.pack(fill="x")

            lbl_name = tk.Label(
                row,
                text=cat_name,
                font=FONT_SMALL,
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD,
                anchor="w"
            )
            lbl_name.pack(side="left", fill="x", expand=True)

            lbl_cnt = tk.Label(
                row,
                text=str(count),
                font=FONT_SMALL_BOLD,
                fg=COLOR_PRIMARY if count > 0 else COLOR_TEXT_MUTED,
                bg="#F0F5F2",
                padx=8,
                pady=2,
                relief="solid",
                bd=1
            )
            lbl_cnt.pack(side="right")

            div = tk.Frame(self.cat_list_frame, bg="#F0F4F1", height=1)
            div.pack(fill="x", pady=2)

        # Render Recent Complaints Table
        for row in self.tree.get_children():
            self.tree.delete(row)

        all_complaints = self.dm.get_all_complaints()

        for i, c in enumerate(all_complaints[:10]):
            status_text = c.get("status", "Pending")
            tag_name = f"row_{c['id']}"

            self.tree.insert(
                "",
                "end",
                values=(
                    c.get("id"),
                    c.get("student_name"),
                    c.get("title"),
                    c.get("location"),
                    c.get("priority"),
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

    def _on_select_complaint(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Select Record",
                "Please select a complaint from the table to view or update.",
                parent=self
            )
            return

        cid = self.tree.item(selected[0])["values"][0]
        ComplaintDetailsDialog(
            self.winfo_toplevel(),
            complaint_id=cid,
            is_admin=True,
            on_update_callback=self.refresh_dashboard
        )
