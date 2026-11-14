"""
views/submit_complaint.py - Screen 4: Submit Complaint for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_SIDEBAR,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StyledButton, APP_NAME
)
from data_manager import DataManager

class CustomLocationDialog(tk.Toplevel):
    """
    Modal popup to input a custom campus location.
    """
    def __init__(self, parent, on_location_added):
        super().__init__(parent)
        self.on_location_added = on_location_added

        self.title("Add Custom Campus Location")
        self.geometry("440x220")
        self.minsize(400, 200)
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)

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
            w, h = 440, 220
            x = px + (pw - w) // 2
            y = py + (ph - h) // 2
            self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

    def _build_ui(self):
        card = tk.Frame(self, bg=COLOR_CARD, padx=22, pady=18, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        lbl_head = tk.Label(
            card,
            text="Add Custom Campus Location",
            font=FONT_TITLE_MED,
            fg=COLOR_SIDEBAR,
            bg=COLOR_CARD
        )
        lbl_head.pack(anchor="w")

        lbl_prompt = tk.Label(
            card,
            text="Enter custom SRMIST building, lab, floor or campus spot:",
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_prompt.pack(anchor="w", pady=(2, 10))

        self.ent_loc = tk.Entry(
            card,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        self.ent_loc.pack(fill="x", ipady=5, pady=(0, 16))
        self.ent_loc.focus_set()
        self.ent_loc.bind("<Return>", lambda e: self._on_add())

        btn_bar = tk.Frame(card, bg=COLOR_CARD)
        btn_bar.pack(fill="x")

        btn_add = StyledButton(
            btn_bar,
            text="✓ Add Location",
            style_type="primary",
            command=self._on_add
        )
        btn_add.pack(side="left", padx=(0, 8))

        btn_cancel = StyledButton(
            btn_bar,
            text="Cancel",
            style_type="secondary",
            command=self.destroy
        )
        btn_cancel.pack(side="left")

    def _on_add(self):
        loc = self.ent_loc.get().strip()
        if not loc:
            messagebox.showerror(
                "Empty Location",
                "Please enter a valid campus location name.",
                parent=self
            )
            return

        self.on_location_added(loc)
        self.destroy()

class SubmitComplaintView(tk.Frame):
    def __init__(self, parent, user_data, on_navigate):
        super().__init__(parent, bg=COLOR_BG)
        self.user_data = user_data
        self.on_navigate = on_navigate
        self.dm = DataManager()

        self._build_ui()

    def _build_ui(self):
        # Outer scrollable container to fit all screens
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

        # Container
        container = tk.Frame(scrollable_frame, bg=COLOR_BG, padx=30, pady=22)
        container.pack(fill="x", expand=True)

        # Header
        top_header = tk.Frame(container, bg=COLOR_BG)
        top_header.pack(fill="x", pady=(0, 16))

        lbl_title = tk.Label(
            top_header,
            text="Submit a Campus Complaint",
            font=FONT_TITLE_LARGE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_title.pack(fill="x")

        lbl_desc = tk.Label(
            top_header,
            text="Report maintenance, electrical, IT, lab, or cleanliness issues directly to the administration.",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_desc.pack(fill="x", pady=(2, 0))

        # Main Card Form
        card = tk.Frame(
            container,
            bg=COLOR_CARD,
            padx=30,
            pady=24,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        card.pack(fill="x")

        # 1. Complaint Title
        lbl_field_title = tk.Label(
            card,
            text="Complaint Title *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_field_title.pack(fill="x", pady=(0, 4))

        self.ent_title = tk.Entry(
            card,
            font=FONT_BODY,
            bg="#FAFCFB",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        self.ent_title.pack(fill="x", ipady=6, pady=(0, 14))

        # 2-Column Row: Category & Location
        row1 = tk.Frame(card, bg=COLOR_CARD)
        row1.pack(fill="x", pady=(0, 14))
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)

        # Category
        cat_box = tk.Frame(row1, bg=COLOR_CARD)
        cat_box.grid(row=0, column=0, sticky="ew", padx=(0, 12))

        lbl_cat = tk.Label(
            cat_box,
            text="Category *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_cat.pack(fill="x", pady=(0, 4))

        self.cb_category = ttk.Combobox(
            cat_box,
            values=self.dm.categories,
            state="readonly",
            font=FONT_BODY
        )
        self.cb_category.set(self.dm.categories[0])
        self.cb_category.pack(fill="x", ipady=4)

        # Location with Custom Location option
        loc_box = tk.Frame(row1, bg=COLOR_CARD)
        loc_box.grid(row=0, column=1, sticky="ew", padx=(12, 0))

        lbl_loc = tk.Label(
            loc_box,
            text="Campus Location *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_loc.pack(fill="x", pady=(0, 4))

        loc_select_row = tk.Frame(loc_box, bg=COLOR_CARD)
        loc_select_row.pack(fill="x")

        self.cb_location = ttk.Combobox(
            loc_select_row,
            values=self._get_location_dropdown_values(),
            state="readonly",
            font=FONT_BODY
        )
        self.cb_location.set(self.dm.locations[0])
        self.cb_location.pack(side="left", fill="x", expand=True, ipady=4)
        self.cb_location.bind("<<ComboboxSelected>>", self._on_location_selected)

        btn_custom_loc = StyledButton(
            loc_select_row,
            text="➕ Custom Location",
            style_type="outline",
            command=self._open_custom_location_dialog
        )
        btn_custom_loc.pack(side="left", padx=(8, 0))

        # 3. Priority Level
        lbl_pri = tk.Label(
            card,
            text="Priority Level *",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_pri.pack(fill="x", pady=(0, 4))

        self.cb_priority = ttk.Combobox(
            card,
            values=self.dm.priorities,
            state="readonly",
            font=FONT_BODY
        )
        self.cb_priority.set("Medium")
        self.cb_priority.pack(fill="x", ipady=4, pady=(0, 14))

        # 4. Larger Description Field
        lbl_desc = tk.Label(
            card,
            text="Detailed Description * (specify room number, equipment details, or problem nature)",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_desc.pack(fill="x", pady=(0, 4))

        desc_container = tk.Frame(card, bg=COLOR_CARD)
        desc_container.pack(fill="x", pady=(0, 20))

        self.txt_desc = tk.Text(
            desc_container,
            font=FONT_BODY,
            fg=COLOR_TEXT_MAIN,
            bg="#FAFCFB",
            height=7,
            wrap="word",
            relief="solid",
            bd=1,
            highlightthickness=0,
            padx=10,
            pady=8
        )
        desc_scroll = ttk.Scrollbar(desc_container, orient="vertical", command=self.txt_desc.yview)
        self.txt_desc.configure(yscrollcommand=desc_scroll.set)

        self.txt_desc.pack(side="left", fill="both", expand=True)
        desc_scroll.pack(side="right", fill="y")

        # Action Buttons
        btn_bar = tk.Frame(card, bg=COLOR_CARD)
        btn_bar.pack(fill="x")

        btn_submit = StyledButton(
            btn_bar,
            text=f"✓ Submit Complaint to {APP_NAME}",
            style_type="primary",
            command=self._on_submit
        )
        btn_submit.pack(side="left", padx=(0, 10))

        btn_clear = StyledButton(
            btn_bar,
            text="Clear Form",
            style_type="secondary",
            command=self._clear_form
        )
        btn_clear.pack(side="left", padx=(0, 10))

        btn_back = StyledButton(
            btn_bar,
            text="Back to Dashboard",
            style_type="outline",
            command=lambda: self.on_navigate("dashboard")
        )
        btn_back.pack(side="left")

    def _get_location_dropdown_values(self):
        return list(self.dm.locations) + ["+ Custom Location..."]

    def _on_location_selected(self, event):
        val = self.cb_location.get()
        if val == "+ Custom Location...":
            self._open_custom_location_dialog()

    def _open_custom_location_dialog(self):
        CustomLocationDialog(
            self.winfo_toplevel(),
            on_location_added=self._on_custom_location_added
        )

    def _on_custom_location_added(self, new_loc):
        ok, res = self.dm.add_custom_location(new_loc)
        # Refresh dropdown values
        self.cb_location.config(values=self._get_location_dropdown_values())
        self.cb_location.set(res)

    def _clear_form(self):
        self.ent_title.delete(0, tk.END)
        self.cb_category.set(self.dm.categories[0])
        self.cb_location.set(self.dm.locations[0])
        self.cb_priority.set("Medium")
        self.txt_desc.delete("1.0", tk.END)

    def _on_submit(self):
        title = self.ent_title.get().strip()
        category = self.cb_category.get().strip()
        location = self.cb_location.get().strip()
        priority = self.cb_priority.get().strip()
        desc = self.txt_desc.get("1.0", "end-1c").strip()

        if location == "+ Custom Location...":
            messagebox.showerror(
                "Invalid Location",
                "Please select or add a specific campus location.",
                parent=self
            )
            return

        username = self.user_data.get("username", "")

        new_complaint, msg = self.dm.add_complaint(
            student_username=username,
            title=title,
            category=category,
            location=location,
            priority=priority,
            description=desc
        )

        if new_complaint:
            # Display clear confirmation popup
            messagebox.showinfo(
                "Complaint Submitted Successfully",
                f"Your complaint has been registered with {APP_NAME}!\n\n"
                f"Ticket ID: {new_complaint['id']}\n"
                f"Title: {new_complaint['title']}\n"
                f"Location: {new_complaint['location']}\n"
                f"Priority: {new_complaint['priority']}\n"
                f"Status: Pending\n\n"
                f"You can track real-time resolution under 'My Complaints'.",
                parent=self
            )
            self._clear_form()
            self.on_navigate("my_complaints")
        else:
            messagebox.showerror("Submission Error", msg, parent=self)
