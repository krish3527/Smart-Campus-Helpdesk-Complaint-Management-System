"""
views/admin_manage.py - Screen 7: Manage Complaints (Admin) for UniResolve
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

class AdminManageView(tk.Frame):
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

        lbl_title = tk.Label(
            top,
            text=f"Manage Campus Complaints - {APP_NAME}",
            font=FONT_TITLE_LARGE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_title.pack(fill="x")

        lbl_sub = tk.Label(
            top,
            text="Review all SRMIST student tickets, assign priorities, inspect equipment/locations, and update resolution statuses.",
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
            width=18
        )
        self.ent_search.pack(side="left", ipady=4, padx=(0, 14))
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_complaints())

        # Category Filter
        lbl_cat = tk.Label(
            filter_card,
            text="Category:",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_cat.pack(side="left", padx=(0, 6))

        cat_opts = ["All"] + self.dm.categories
        self.cb_cat = ttk.Combobox(
            filter_card,
            values=cat_opts,
            state="readonly",
            width=16,
            font=FONT_BODY
        )
        self.cb_cat.set("All")
        self.cb_cat.pack(side="left", ipady=3, padx=(0, 14))
        self.cb_cat.bind("<<ComboboxSelected>>", lambda e: self.load_complaints())

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
            width=12,
            font=FONT_BODY
        )
        self.cb_status.set("All")
        self.cb_status.pack(side="left", ipady=3, padx=(0, 14))
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
            width=10,
            font=FONT_BODY
        )
        self.cb_pri.set("All")
        self.cb_pri.pack(side="left", ipady=3, padx=(0, 14))
        self.cb_pri.bind("<<ComboboxSelected>>", lambda e: self.load_complaints())

        # Reset button
        btn_reset = StyledButton(
            filter_card,
            text="Reset Filters",
            style_type="secondary",
            command=self._reset_filters
        )
        btn_reset.pack(side="left")

        # 3. Main Complaints Table Card
        table_card = tk.Frame(
            self,
            bg=COLOR_CARD,
            padx=18,
            pady=16,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        table_card.pack(fill="both", expand=True, padx=28, pady=(0, 14))

        table_header = tk.Frame(table_card, bg=COLOR_CARD)
        table_header.pack(fill="x", pady=(0, 10))

        self.lbl_count = tk.Label(
            table_header,
            text="Total: 0 complaints",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        self.lbl_count.pack(side="left")

        lbl_hint = tk.Label(
            table_header,
            text="(Double click any record to open full inspection & update dialog)",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_hint.pack(side="left", padx=10)

        # Table
        columns = ("id", "student", "title", "category", "location", "priority", "date", "status")
        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("id", text="Complaint ID", anchor="center")
        self.tree.heading("student", text="Student Name", anchor="w")
        self.tree.heading("title", text="Title", anchor="w")
        self.tree.heading("category", text="Category", anchor="w")
        self.tree.heading("location", text="Location", anchor="w")
        self.tree.heading("priority", text="Priority", anchor="center")
        self.tree.heading("date", text="Date", anchor="center")
        self.tree.heading("status", text="Status", anchor="center")

        self.tree.column("id", width=95, minwidth=80, anchor="center")
        self.tree.column("student", width=130, minwidth=100, anchor="w")
        self.tree.column("title", width=210, minwidth=160, anchor="w")
        self.tree.column("category", width=140, minwidth=110, anchor="w")
        self.tree.column("location", width=130, minwidth=100, anchor="w")
        self.tree.column("priority", width=85, minwidth=70, anchor="center")
        self.tree.column("date", width=95, minwidth=80, anchor="center")
        self.tree.column("status", width=115, minwidth=95, anchor="center")

        tree_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._on_view_details())

        # 4. Quick Action Toolbar Card (Below Table)
        action_card = tk.Frame(
            self,
            bg=COLOR_CARD,
            padx=18,
            pady=12,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        action_card.pack(fill="x", padx=28, pady=(0, 16))

        # Left: View Details button
        btn_details = StyledButton(
            action_card,
            text="🔍 View Full Details",
            style_type="secondary",
            command=self._on_view_details
        )
        btn_details.pack(side="left", padx=(0, 14))

        # Center/Right: Quick Status Update Panel
        sep = tk.Frame(action_card, bg=COLOR_BORDER, width=1, height=26)
        sep.pack(side="left", padx=(0, 14))

        lbl_quick_st = tk.Label(
            action_card,
            text="Quick Status Update:",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_quick_st.pack(side="left", padx=(0, 8))

        self.cb_quick_status = ttk.Combobox(
            action_card,
            values=self.dm.statuses,
            state="readonly",
            width=13,
            font=FONT_BODY
        )
        self.cb_quick_status.set("In Progress")
        self.cb_quick_status.pack(side="left", ipady=3, padx=(0, 8))

        btn_update_quick = StyledButton(
            action_card,
            text="✓ Set Status",
            style_type="primary",
            command=self._on_quick_status_update
        )
        btn_update_quick.pack(side="left", padx=(0, 14))

        # Rightmost: Refresh
        btn_refresh = StyledButton(
            action_card,
            text="🔄 Refresh",
            style_type="outline",
            command=self.load_complaints
        )
        btn_refresh.pack(side="right")

    def _reset_filters(self):
        self.ent_search.delete(0, tk.END)
        self.cb_cat.set("All")
        self.cb_status.set("All")
        self.cb_pri.set("All")
        self.load_complaints()

    def load_complaints(self):
        """Fetch all complaints, apply filters, and populate table."""
        all_complaints = self.dm.get_all_complaints()

        query = self.ent_search.get().strip()
        cat = self.cb_cat.get()
        status = self.cb_status.get()
        pri = self.cb_pri.get()

        filtered = self.dm.filter_complaints(
            all_complaints,
            search_query=query,
            category=cat,
            status=status,
            priority=pri
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
                    c.get("student_name"),
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

        self.lbl_count.config(text=f"Showing {len(filtered)} of {len(all_complaints)} complaints")

    def _on_view_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Select Record",
                "Please select a complaint to view full details and update resolution remarks.",
                parent=self
            )
            return

        cid = self.tree.item(selected[0])["values"][0]
        ComplaintDetailsDialog(
            self.winfo_toplevel(),
            complaint_id=cid,
            is_admin=True,
            on_update_callback=self.load_complaints
        )

    def _on_quick_status_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Select Record",
                "Please select a complaint from the table first.",
                parent=self
            )
            return

        cid = self.tree.item(selected[0])["values"][0]
        new_status = self.cb_quick_status.get().strip()

        success, msg = self.dm.update_complaint_status(cid, new_status)
        if success:
            messagebox.showinfo("Status Updated", msg, parent=self)
            self.load_complaints()
        else:
            messagebox.showerror("Update Error", msg, parent=self)
