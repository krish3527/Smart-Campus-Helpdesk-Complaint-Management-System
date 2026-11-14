"""
views/my_complaints.py - Screen 5: My Complaints for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_PENDING, COLOR_IN_PROGRESS, COLOR_RESOLVED, COLOR_DANGER,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StyledButton, APP_NAME
)
from data_manager import DataManager
from views.details_dialog import ComplaintDetailsDialog

class MyComplaintsView(tk.Frame):
    def __init__(self, parent, user_data, on_navigate):
        super().__init__(parent, bg=COLOR_BG)
        self.user_data = user_data
        self.on_navigate = on_navigate
        self.dm = DataManager()

        self._build_ui()
        self.load_complaints()

    def _build_ui(self):
        # 1. Header
        top = tk.Frame(self, bg=COLOR_BG, padx=28, pady=20)
        top.pack(fill="x")

        head_row = tk.Frame(top, bg=COLOR_BG)
        head_row.pack(fill="x")

        lbl_title = tk.Label(
            head_row,
            text="My Submitted Complaints",
            font=FONT_TITLE_LARGE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_title.pack(side="left")

        btn_new = StyledButton(
            head_row,
            text="➕ New Complaint",
            style_type="primary",
            command=lambda: self.on_navigate("submit_complaint")
        )
        btn_new.pack(side="right")

        lbl_sub = tk.Label(
            top,
            text=f"Review, search, and track live resolution updates for all your tickets in {APP_NAME}.",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_sub.pack(fill="x", pady=(4, 0))

        # 2. Filter & Search Toolbar Card
        filter_card = tk.Frame(
            self,
            bg=COLOR_CARD,
            padx=18,
            pady=14,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        filter_card.pack(fill="x", padx=28, pady=(0, 14))

        # Search Bar
        lbl_search = tk.Label(
            filter_card,
            text="Search:",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_search.pack(side="left", padx=(0, 6))

        self.ent_search = tk.Entry(
            filter_card,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            width=22
        )
        self.ent_search.pack(side="left", ipady=4, padx=(0, 16))
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_complaints())

        # Status Filter
        lbl_status = tk.Label(
            filter_card,
            text="Status:",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_status.pack(side="left", padx=(0, 6))

        status_opts = ["All"] + self.dm.statuses
        self.cb_status = ttk.Combobox(
            filter_card,
            values=status_opts,
            state="readonly",
            width=13,
            font=FONT_BODY
        )
        self.cb_status.set("All")
        self.cb_status.pack(side="left", ipady=3, padx=(0, 16))
        self.cb_status.bind("<<ComboboxSelected>>", lambda e: self.load_complaints())

        # Priority Filter
        lbl_pri = tk.Label(
            filter_card,
            text="Priority:",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_pri.pack(side="left", padx=(0, 6))

        pri_opts = ["All"] + self.dm.priorities
        self.cb_pri = ttk.Combobox(
            filter_card,
            values=pri_opts,
            state="readonly",
            width=11,
            font=FONT_BODY
        )
        self.cb_pri.set("All")
        self.cb_pri.pack(side="left", ipady=3, padx=(0, 16))
        self.cb_pri.bind("<<ComboboxSelected>>", lambda e: self.load_complaints())

        # Reset button
        btn_reset = StyledButton(
            filter_card,
            text="Reset Filters",
            style_type="secondary",
            command=self._reset_filters
        )
        btn_reset.pack(side="left")

        # 3. Complaints Table Card
        table_card = tk.Frame(
            self,
            bg=COLOR_CARD,
            padx=18,
            pady=16,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        table_card.pack(fill="both", expand=True, padx=28, pady=(0, 16))

        table_header = tk.Frame(table_card, bg=COLOR_CARD)
        table_header.pack(fill="x", pady=(0, 10))

        self.lbl_count = tk.Label(
            table_header,
            text="Showing 0 complaints",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        self.lbl_count.pack(side="left")

        lbl_hint = tk.Label(
            table_header,
            text="(Double click any record to view full details and technician remarks)",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_hint.pack(side="left", padx=10)

        # Treeview
        tree_container = tk.Frame(table_card, bg=COLOR_CARD)
        tree_container.pack(fill="both", expand=True)

        columns = ("id", "title", "category", "location", "priority", "date", "status")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="Complaint ID", anchor="center")
        self.tree.heading("title", text="Title", anchor="w")
        self.tree.heading("category", text="Category", anchor="w")
        self.tree.heading("location", text="Campus Location", anchor="w")
        self.tree.heading("priority", text="Priority", anchor="center")
        self.tree.heading("date", text="Date Filed", anchor="center")
        self.tree.heading("status", text="Status", anchor="center")

        self.tree.column("id", width=100, minwidth=80, anchor="center")
        self.tree.column("title", width=250, minwidth=180, anchor="w")
        self.tree.column("category", width=160, minwidth=120, anchor="w")
        self.tree.column("location", width=150, minwidth=110, anchor="w")
        self.tree.column("priority", width=90, minwidth=80, anchor="center")
        self.tree.column("date", width=100, minwidth=90, anchor="center")
        self.tree.column("status", width=120, minwidth=100, anchor="center")

        tree_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._view_details())

        # Bottom Actions Bar
        bottom_bar = tk.Frame(table_card, bg=COLOR_CARD)
        bottom_bar.pack(fill="x", pady=(12, 0))

        btn_view = StyledButton(
            bottom_bar,
            text="🔍 View Complaint Details",
            style_type="primary",
            command=self._view_details
        )
        btn_view.pack(side="left", padx=(0, 10))

        btn_refresh = StyledButton(
            bottom_bar,
            text="🔄 Refresh List",
            style_type="secondary",
            command=self.load_complaints
        )
        btn_refresh.pack(side="left")

    def _reset_filters(self):
        self.ent_search.delete(0, tk.END)
        self.cb_status.set("All")
        self.cb_pri.set("All")
        self.load_complaints()

    def load_complaints(self):
        """Filter and render student's complaints."""
        username = self.user_data.get("username", "")
        student_complaints = self.dm.get_complaints_by_student(username)

        query = self.ent_search.get().strip()
        status = self.cb_status.get()
        priority = self.cb_pri.get()

        filtered = self.dm.filter_complaints(
            student_complaints,
            search_query=query,
            status=status,
            priority=priority
        )

        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, c in enumerate(filtered):
            status_text = c.get("status", "Pending")
            tag_name = f"st_{c['id']}"

            self.tree.insert(
                "",
                "end",
                values=(
                    c.get("id"),
                    c.get("title"),
                    c.get("category"),
                    c.get("location"),
                    c.get("priority"),
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

        self.lbl_count.config(text=f"Showing {len(filtered)} of {len(student_complaints)} complaints")

    def _view_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Select Complaint",
                "Please select a complaint from the table to view full details.",
                parent=self
            )
            return

        cid = self.tree.item(selected[0])["values"][0]
        ComplaintDetailsDialog(
            self.winfo_toplevel(),
            complaint_id=cid,
            is_admin=False,
            on_update_callback=self.load_complaints
        )
