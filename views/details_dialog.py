"""
views/details_dialog.py - Reusable Complaint Details Window for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_PENDING, COLOR_IN_PROGRESS, COLOR_RESOLVED, COLOR_DANGER,
    FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_SMALL_BOLD,
    StyledButton, APP_NAME
)
from data_manager import DataManager

class ComplaintDetailsDialog(tk.Toplevel):
    def __init__(self, parent, complaint_id, is_admin=False, on_update_callback=None):
        super().__init__(parent)
        self.dm = DataManager()
        self.complaint_id = complaint_id
        self.is_admin = is_admin
        self.on_update_callback = on_update_callback

        self.complaint = self.dm.get_complaint_by_id(complaint_id)

        self.title(f"{APP_NAME} - Ticket Record #{complaint_id}")
        self.geometry("640x700")
        self.minsize(580, 600)
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent window
        self._center_window(parent)

        if not self.complaint:
            messagebox.showerror("Error", f"Complaint {complaint_id} could not be loaded.", parent=self)
            self.destroy()
            return

        self._build_ui()

    def _center_window(self, parent):
        self.update_idletasks()
        try:
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            w = 640
            h = 700
            x = px + (pw - w) // 2
            y = py + (ph - h) // 2
            self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

    def _get_status_color(self, status):
        if status == "Pending":
            return COLOR_PENDING
        elif status == "In Progress":
            return COLOR_IN_PROGRESS
        elif status == "Resolved":
            return COLOR_RESOLVED
        return COLOR_TEXT_MUTED

    def _get_priority_color(self, priority):
        if priority == "High":
            return COLOR_DANGER
        elif priority == "Medium":
            return COLOR_PENDING
        return COLOR_RESOLVED

    def _build_ui(self):
        # 1. Header Card
        header = tk.Frame(self, bg=COLOR_CARD, padx=20, pady=16, highlightbackground=COLOR_BORDER, highlightthickness=1)
        header.pack(fill="x", padx=16, pady=(16, 10))

        # Top row: ID + Status + Priority Badges
        top_row = tk.Frame(header, bg=COLOR_CARD)
        top_row.pack(fill="x")

        lbl_id = tk.Label(
            top_row,
            text=f"Ticket #{self.complaint['id']}",
            font=FONT_TITLE_MED,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD
        )
        lbl_id.pack(side="left")

        # Priority badge
        pri = self.complaint.get("priority", "Low")
        lbl_pri = tk.Label(
            top_row,
            text=f"  Priority: {pri}  ",
            font=FONT_SMALL_BOLD,
            fg="#FFFFFF",
            bg=self._get_priority_color(pri),
            padx=4,
            pady=2
        )
        lbl_pri.pack(side="right", padx=(6, 0))

        # Status badge
        st = self.complaint.get("status", "Pending")
        self.lbl_status_badge = tk.Label(
            top_row,
            text=f"  {st.upper()}  ",
            font=FONT_SMALL_BOLD,
            fg="#FFFFFF",
            bg=self._get_status_color(st),
            padx=6,
            pady=2
        )
        self.lbl_status_badge.pack(side="right")

        # Title
        lbl_title = tk.Label(
            header,
            text=self.complaint.get("title", ""),
            font=FONT_SECTION,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD,
            anchor="w",
            wraplength=560,
            justify="left"
        )
        lbl_title.pack(fill="x", pady=(8, 0))

        # 2. Scrollable Body
        canvas_container = tk.Frame(self, bg=COLOR_BG)
        canvas_container.pack(fill="both", expand=True, padx=16, pady=4)

        canvas = tk.Canvas(canvas_container, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        body = tk.Frame(canvas, bg=COLOR_BG)

        body.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=body, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scroll support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Details Grid Card
        info_card = tk.Frame(body, bg=COLOR_CARD, padx=18, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        info_card.pack(fill="x", pady=6)

        lbl_info_heading = tk.Label(
            info_card,
            text="Complaint Metadata",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_info_heading.pack(anchor="w", pady=(0, 10))

        # 2-column info layout
        grid_frame = tk.Frame(info_card, bg=COLOR_CARD)
        grid_frame.pack(fill="x")
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        def add_info_row(row_idx, col_idx, label, val):
            box = tk.Frame(grid_frame, bg=COLOR_CARD)
            box.grid(row=row_idx, column=col_idx, sticky="w", padx=6, pady=4)
            l = tk.Label(box, text=label, font=FONT_SMALL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
            l.pack(anchor="w")
            v = tk.Label(box, text=val, font=FONT_BODY_BOLD, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
            v.pack(anchor="w")

        add_info_row(0, 0, "Category", self.complaint.get("category", "-"))
        add_info_row(0, 1, "Location", self.complaint.get("location", "-"))
        add_info_row(1, 0, "Date Filed", self.complaint.get("date", "-"))
        add_info_row(1, 1, "Current Status", self.complaint.get("status", "-"))

        # Student Details Card
        student_card = tk.Frame(body, bg=COLOR_CARD, padx=18, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        student_card.pack(fill="x", pady=6)

        lbl_stu_heading = tk.Label(
            student_card,
            text="Student Information (SRMIST)",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_stu_heading.pack(anchor="w", pady=(0, 10))

        stu_grid = tk.Frame(student_card, bg=COLOR_CARD)
        stu_grid.pack(fill="x")
        stu_grid.columnconfigure(0, weight=1)
        stu_grid.columnconfigure(1, weight=1)

        def add_stu_row(row_idx, col_idx, label, val):
            box = tk.Frame(stu_grid, bg=COLOR_CARD)
            box.grid(row=row_idx, column=col_idx, sticky="w", padx=6, pady=4)
            l = tk.Label(box, text=label, font=FONT_SMALL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
            l.pack(anchor="w")
            v = tk.Label(box, text=val, font=FONT_BODY_BOLD, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
            v.pack(anchor="w")

        # Fetch student details
        student_info = self.dm.get_student(self.complaint.get("student_username", ""))
        student_name = self.complaint.get("student_name", "Student")
        reg_no = self.complaint.get("student_reg", student_info.get("reg_no", "-") if student_info else "-")
        dept = self.complaint.get("student_dept", student_info.get("department", "-") if student_info else "-")
        email = student_info.get("email", "-") if student_info else "-"

        add_stu_row(0, 0, "Student Name", student_name)
        add_stu_row(0, 1, "Registration No.", reg_no)
        add_stu_row(1, 0, "Department", dept)
        add_stu_row(1, 1, "SRMIST Email", email)

        # Description Card
        desc_card = tk.Frame(body, bg=COLOR_CARD, padx=18, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        desc_card.pack(fill="x", pady=6)

        lbl_desc_heading = tk.Label(
            desc_card,
            text="Complaint Description",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_desc_heading.pack(anchor="w", pady=(0, 6))

        desc_text = tk.Text(
            desc_card,
            font=FONT_BODY,
            fg=COLOR_TEXT_MAIN,
            bg="#F9FBFA",
            height=4,
            wrap="word",
            relief="solid",
            bd=1,
            highlightthickness=0,
            padx=8,
            pady=8
        )
        desc_text.insert("1.0", self.complaint.get("description", "No description provided."))
        desc_text.config(state="disabled")
        desc_text.pack(fill="x")

        # Admin Remarks Card (Visible to all, editable only by admin)
        remarks_card = tk.Frame(body, bg=COLOR_CARD, padx=18, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        remarks_card.pack(fill="x", pady=6)

        lbl_rem_heading = tk.Label(
            remarks_card,
            text="Administrative Action & Remarks",
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        )
        lbl_rem_heading.pack(anchor="w", pady=(0, 6))

        if self.is_admin:
            # Admin can edit remarks and status
            lbl_status_prompt = tk.Label(
                remarks_card,
                text="Update Status:",
                font=FONT_BODY_BOLD,
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD
            )
            lbl_status_prompt.pack(anchor="w", pady=(4, 2))

            self.cb_status = ttk.Combobox(
                remarks_card,
                values=self.dm.statuses,
                state="readonly",
                font=FONT_BODY
            )
            self.cb_status.set(self.complaint.get("status", "Pending"))
            self.cb_status.pack(fill="x", pady=(0, 8))

            lbl_note_prompt = tk.Label(
                remarks_card,
                text="Resolution Notes / Remarks:",
                font=FONT_BODY_BOLD,
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD
            )
            lbl_note_prompt.pack(anchor="w", pady=(4, 2))

            self.txt_remarks = tk.Text(
                remarks_card,
                font=FONT_BODY,
                fg=COLOR_TEXT_MAIN,
                bg="#FFFFFF",
                height=3,
                wrap="word",
                relief="solid",
                bd=1,
                highlightthickness=0,
                padx=8,
                pady=6
            )
            existing_remarks = self.complaint.get("admin_remarks", "")
            if existing_remarks:
                self.txt_remarks.insert("1.0", existing_remarks)
            self.txt_remarks.pack(fill="x", pady=(0, 8))

            btn_save = StyledButton(
                remarks_card,
                text="💾 Save Status & Remarks",
                style_type="primary",
                command=self._on_save_admin_update
            )
            btn_save.pack(anchor="e", pady=(4, 0))
        else:
            # Student view - read only remarks
            cur_remarks = self.complaint.get("admin_remarks", "")
            if not cur_remarks:
                cur_remarks = "No administrative remarks added yet. Status will be updated once facility staff inspects this ticket."

            lbl_rem = tk.Label(
                remarks_card,
                text=cur_remarks,
                font=FONT_BODY,
                fg=COLOR_TEXT_MAIN,
                bg="#F9FBFA",
                anchor="w",
                justify="left",
                wraplength=520,
                padx=10,
                pady=8,
                relief="solid",
                bd=1
            )
            lbl_rem.pack(fill="x")

        # 3. Bottom Close Button
        bottom_bar = tk.Frame(self, bg=COLOR_BG, padx=16, pady=12)
        bottom_bar.pack(fill="x", side="bottom")

        btn_close = StyledButton(
            bottom_bar,
            text="Close Window",
            style_type="secondary",
            command=self.destroy
        )
        btn_close.pack(side="right")

    def _on_save_admin_update(self):
        new_status = self.cb_status.get().strip()
        new_remarks = self.txt_remarks.get("1.0", "end-1c").strip()

        success, msg = self.dm.update_complaint_status(self.complaint_id, new_status, new_remarks)
        if success:
            self.lbl_status_badge.config(
                text=f"  {new_status.upper()}  ",
                bg=self._get_status_color(new_status)
            )
            messagebox.showinfo("Success", msg, parent=self)
            if self.on_update_callback:
                self.on_update_callback()
        else:
            messagebox.showerror("Update Failed", msg, parent=self)
