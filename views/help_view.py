"""
views/help_view.py - Screen 8: Help & FAQ for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk
from ui_components import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_PRIMARY, COLOR_SIDEBAR, COLOR_PENDING, COLOR_IN_PROGRESS, COLOR_RESOLVED,
    FONT_TITLE_LARGE, FONT_TITLE_MED, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_SMALL_BOLD, StyledButton, APP_NAME, APP_TAGLINE
)

class HelpView(tk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent, bg=COLOR_BG)
        self.user_data = user_data

        self._build_ui()

    def _build_ui(self):
        # Outer scrollable frame
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
        container = tk.Frame(scrollable_frame, bg=COLOR_BG, padx=28, pady=24)
        container.pack(fill="x", expand=True)

        # Header
        lbl_title = tk.Label(
            container,
            text=f"{APP_NAME} Help Center & Frequently Asked Questions",
            font=FONT_TITLE_LARGE,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_title.pack(fill="x")

        lbl_sub = tk.Label(
            container,
            text=f"SRMIST Campus Facility & Helpdesk Operations   •   {APP_TAGLINE}",
            font=FONT_BODY,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG,
            anchor="w"
        )
        lbl_sub.pack(fill="x", pady=(3, 16))

        # FAQs
        faqs = [
            (
                "1. How can I submit a complaint?",
                f"Click 'Submit Complaint' from the left sidebar navigation in {APP_NAME}. Provide a clear title, select the relevant category (Infrastructure, Electrical, IT & Network, Cleanliness, or Classroom/Lab), choose the campus location (e.g. TP1, TP2, Java Canteen, University Building, TP Ganeshan, Vendhar Square, or add a Custom Location), specify a priority, and write a detailed description. A unique ticket ID (e.g. CMP006) will be generated automatically."
            ),
            (
                "2. How can I track my complaint?",
                "Navigate to 'My Complaints' from the sidebar. You can view all complaints you have logged, search by Ticket ID or title, and filter by status. Double-clicking any record opens a detailed view showing administrative updates and technician resolution notes."
            ),
            (
                "3. What do the complaint statuses mean?",
                "• Pending (Amber): The complaint has been registered and is awaiting facility staff review.\n"
                "• In Progress (Blue): The campus facility team has assigned a technician who is actively working on the resolution.\n"
                "• Resolved (Green): The issue has been repaired or verified, and the ticket is successfully closed."
            ),
            (
                "4. Who can resolve my complaint?",
                "Complaints are reviewed and managed by authorized SRMIST Campus Facility Administrators and department supervisors. Only authenticated administrators have authority to inspect campus complaints and update resolution statuses."
            ),
            (
                "5. What should I do if my complaint remains pending?",
                "If a high-priority complaint remains in 'Pending' status for more than 48 hours, visit the Campus Helpdesk Office in the Administrative Block (Room 104) or contact the facility helpdesk phone line with your Complaint ID for prompt escalation."
            )
        ]

        # FAQs Card Container
        faq_container = tk.Frame(container, bg=COLOR_BG)
        faq_container.pack(fill="x", pady=(0, 16))

        for q, a in faqs:
            card = tk.Frame(
                faq_container,
                bg=COLOR_CARD,
                padx=20,
                pady=14,
                highlightbackground=COLOR_BORDER,
                highlightthickness=1,
                bd=0
            )
            card.pack(fill="x", pady=(0, 10))

            lbl_q = tk.Label(
                card,
                text=q,
                font=FONT_TITLE_MED,
                fg=COLOR_SIDEBAR,
                bg=COLOR_CARD,
                anchor="w"
            )
            lbl_q.pack(fill="x")

            lbl_a = tk.Label(
                card,
                text=a,
                font=FONT_BODY,
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD,
                anchor="w",
                justify="left",
                wraplength=760
            )
            lbl_a.pack(fill="x", pady=(6, 0))

        # SRMIST Helpdesk Contact Information Card
        contact_card = tk.Frame(
            container,
            bg=COLOR_CARD,
            padx=22,
            pady=18,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0
        )
        contact_card.pack(fill="x", pady=(0, 20))

        lbl_contact_head = tk.Label(
            contact_card,
            text=f"📞 {APP_NAME} & SRMIST Facility Office Contact Information",
            font=FONT_TITLE_MED,
            fg=COLOR_SIDEBAR,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_contact_head.pack(fill="x", pady=(0, 12))

        contact_grid = tk.Frame(contact_card, bg=COLOR_CARD)
        contact_grid.pack(fill="x")
        contact_grid.columnconfigure(0, weight=1)
        contact_grid.columnconfigure(1, weight=1)

        def add_contact_box(r, c, title, info):
            box = tk.Frame(contact_grid, bg="#F7FAF8", padx=12, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
            box.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

            t = tk.Label(box, text=title, font=FONT_SMALL_BOLD, fg=COLOR_PRIMARY, bg="#F7FAF8", anchor="w")
            t.pack(fill="x")
            v = tk.Label(box, text=info, font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg="#F7FAF8", anchor="w", justify="left")
            v.pack(fill="x", pady=(2, 0))

        add_contact_box(0, 0, "📍 Helpdesk Office", "Ground Floor, University Building\nRoom 104, SRMIST Main Campus, Kattankulathur")
        add_contact_box(0, 1, "⏰ Operating Hours", "Monday – Friday: 9:00 AM – 5:00 PM\nSaturday: 9:00 AM – 1:00 PM (Emergency facility only)")
        add_contact_box(1, 0, "✉️ Email Support", "helpdesk@srmist.edu.in\nfacility.admin@srmist.edu.in")
        add_contact_box(1, 1, "☎️ Helpline & Extensions", "SRMIST EPABX: (044) 2745-5510, Ext: 402/405\nDirect Helpline: +91 98765 43210")
