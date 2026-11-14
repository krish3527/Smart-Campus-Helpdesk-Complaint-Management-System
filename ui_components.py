"""
ui_components.py - Reusable UI Styling and Custom Widgets for UniResolve
Your Campus. Your Voice. Our Resolution.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import glob
from PIL import Image, ImageTk

# --- Color Palette (Theme Guidelines) ---
COLOR_SIDEBAR = "#173D2D"         # Deep forest green
COLOR_PRIMARY = "#238653"         # Primary campus green
COLOR_PRIMARY_HOVER = "#1B6E43"   # Hover state
COLOR_PRIMARY_ACTIVE = "#165936"  # Pressed state
COLOR_BG = "#F4F7F5"              # Light crisp background
COLOR_CARD = "#FFFFFF"            # White card background
COLOR_BORDER = "#D9E2DC"          # Subtle border
COLOR_TEXT_MAIN = "#26352C"       # Dark green-slate main text
COLOR_TEXT_MUTED = "#78857D"      # Secondary gray-green text
COLOR_PENDING = "#E9A23B"         # Warm amber/orange
COLOR_IN_PROGRESS = "#397CC5"     # Trustworthy blue
COLOR_RESOLVED = "#238653"        # Success green
COLOR_DANGER = "#D9534F"          # Soft danger red
COLOR_DANGER_HOVER = "#C9302C"

# --- Application Identity ---
APP_NAME = "UniResolve"
APP_TAGLINE = "Your Campus. Your Voice. Our Resolution."

# --- Typography Defaults ---
FONT_FAMILY = "Segoe UI"
FONT_TITLE_LARGE = (FONT_FAMILY, 16, "bold")
FONT_TITLE_MED = (FONT_FAMILY, 13, "bold")
FONT_SECTION = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 10)
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_SMALL = (FONT_FAMILY, 9)
FONT_SMALL_BOLD = (FONT_FAMILY, 9, "bold")
FONT_STAT_NUM = (FONT_FAMILY, 22, "bold")

# Cache to prevent garbage collection of Tkinter images
_PHOTO_CACHE = {}

def hex_to_rgb(hex_str):
    """Converts hex color '#RRGGBB' to an RGB tuple (r, g, b)."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def load_app_logo(max_width, max_height, bg_color=None):
    """
    Finds and loads the user's uploaded logo while strictly maintaining original proportions.
    If bg_color is given (e.g. hex '#173D2D' or '#FFFFFF'), smoothly blends transparent pixels
    against that exact background color for anti-aliasing.
    Uses Pillow with high-quality LANCZOS resampling.
    """
    cache_key = f"{max_width}x{max_height}_{bg_color}"
    if cache_key in _PHOTO_CACHE:
        return _PHOTO_CACHE[cache_key]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")

    # Priority candidate paths
    candidate_paths = [
        os.path.join(assets_dir, "logo.png"),
        os.path.join(assets_dir, "logo.jpg"),
        os.path.join(assets_dir, "logo.jpeg"),
        os.path.join(assets_dir, "uniresolve_logo.png"),
        os.path.join(base_dir, "logo.png"),
        os.path.join(base_dir, "logo.jpg"),
        os.path.join(assets_dir, "logo_small.png")
    ]

    for path in candidate_paths:
        if os.path.exists(path) and os.path.isfile(path):
            try:
                img = Image.open(path)
                orig_w, orig_h = img.size
                if orig_w <= 0 or orig_h <= 0:
                    continue

                # Preserve alpha blending if background color is specified
                if bg_color and img.mode in ("RGBA", "LA", "P"):
                    img_rgba = img.convert("RGBA")
                    rgb = hex_to_rgb(bg_color)
                    canvas = Image.new("RGBA", img_rgba.size, (*rgb, 255))
                    img = Image.alpha_composite(canvas, img_rgba)

                # Compute scale ratio to preserve exact aspect ratio
                ratio = min(max_width / orig_w, max_height / orig_h)
                new_w = max(1, int(orig_w * ratio))
                new_h = max(1, int(orig_h * ratio))

                resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(resized)
                _PHOTO_CACHE[cache_key] = photo
                return photo
            except Exception:
                pass

    return None

def setup_app_styles():
    """Configure modern ttk styles for treeviews, scrollbars, comboboxes, etc."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Treeview Styling
    style.configure(
        "Custom.Treeview",
        background="#FFFFFF",
        foreground=COLOR_TEXT_MAIN,
        rowheight=32,
        fieldbackground="#FFFFFF",
        font=FONT_BODY,
        borderwidth=0
    )
    style.configure(
        "Custom.Treeview.Heading",
        background="#E8EFEA",
        foreground=COLOR_TEXT_MAIN,
        font=FONT_SMALL_BOLD,
        padding=7,
        borderwidth=1,
        relief="flat"
    )
    style.map(
        "Custom.Treeview.Heading",
        background=[("active", "#DCE6DE")]
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", "#238653")],
        foreground=[("selected", "#FFFFFF")]
    )

    # Combobox Styling
    style.configure(
        "TCombobox",
        fieldbackground="#FFFFFF",
        background="#FFFFFF",
        foreground=COLOR_TEXT_MAIN,
        arrowcolor=COLOR_TEXT_MAIN,
        padding=6,
        font=FONT_BODY
    )

    # Scrollbar Styling
    style.configure(
        "Vertical.TScrollbar",
        background="#E0E6E2",
        troughcolor=COLOR_BG,
        borderwidth=0,
        arrowcolor=COLOR_TEXT_MAIN
    )

class StatCard(tk.Frame):
    """
    Stat card showing count, title, indicator accent bar, and subtle subtitle.
    """
    def __init__(self, parent, title, value, accent_color=COLOR_PRIMARY, subtitle="", **kwargs):
        super().__init__(
            parent,
            bg=COLOR_CARD,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0,
            **kwargs
        )
        self.accent_color = accent_color

        # Left colored accent line
        accent_bar = tk.Frame(self, bg=accent_color, width=5)
        accent_bar.pack(side="left", fill="y")

        # Content container
        content = tk.Frame(self, bg=COLOR_CARD, padx=16, pady=12)
        content.pack(side="left", fill="both", expand=True)

        # Title
        lbl_title = tk.Label(
            content,
            text=title.upper(),
            font=FONT_SMALL_BOLD,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD,
            anchor="w"
        )
        lbl_title.pack(fill="x")

        # Number value
        self.lbl_val = tk.Label(
            content,
            text=str(value),
            font=FONT_STAT_NUM,
            fg=accent_color,
            bg=COLOR_CARD,
            anchor="w"
        )
        self.lbl_val.pack(fill="x", pady=(2, 0))

        # Optional subtitle
        if subtitle:
            lbl_sub = tk.Label(
                content,
                text=subtitle,
                font=FONT_SMALL,
                fg=COLOR_TEXT_MUTED,
                bg=COLOR_CARD,
                anchor="w"
            )
            lbl_sub.pack(fill="x")

    def update_value(self, new_val):
        self.lbl_val.config(text=str(new_val))

class StyledButton(tk.Button):
    """
    Standard button with clean hover effects and predefined styles.
    """
    def __init__(self, parent, text, command=None, style_type="primary", width=None, **kwargs):
        self.style_type = style_type

        if style_type == "primary":
            bg = COLOR_PRIMARY
            fg = "#FFFFFF"
            self.hover_bg = COLOR_PRIMARY_HOVER
            self.active_bg = COLOR_PRIMARY_ACTIVE
        elif style_type == "secondary":
            bg = "#E9EFEA"
            fg = COLOR_TEXT_MAIN
            self.hover_bg = "#DCE4DE"
            self.active_bg = "#CFD9D1"
        elif style_type == "outline":
            bg = "#FFFFFF"
            fg = COLOR_PRIMARY
            self.hover_bg = "#F0F5F2"
            self.active_bg = "#E2EAE5"
        elif style_type == "danger":
            bg = COLOR_DANGER
            fg = "#FFFFFF"
            self.hover_bg = COLOR_DANGER_HOVER
            self.active_bg = "#A9221F"
        elif style_type == "sidebar":
            bg = "transparent"
            fg = "#E2EAE5"
            self.hover_bg = "#1F4E3A"
            self.active_bg = "#235B43"
        else:
            bg = "#FFFFFF"
            fg = COLOR_TEXT_MAIN
            self.hover_bg = "#F0F0F0"
            self.active_bg = "#E0E0E0"

        btn_kwargs = {
            "text": text,
            "command": command,
            "font": FONT_BODY_BOLD if style_type != "outline" else FONT_BODY,
            "bg": bg if bg != "transparent" else COLOR_SIDEBAR,
            "fg": fg,
            "activebackground": self.active_bg,
            "activeforeground": fg,
            "relief": "flat",
            "bd": 0,
            "cursor": "hand2",
            "padx": 14,
            "pady": 7
        }
        if width:
            btn_kwargs["width"] = width

        btn_kwargs.update(kwargs)
        super().__init__(parent, **btn_kwargs)

        self.normal_bg = btn_kwargs["bg"]

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.config(bg=self.hover_bg)

    def _on_leave(self, event):
        self.config(bg=self.normal_bg)

class Sidebar(tk.Frame):
    """
    Standard left navigation sidebar for UniResolve Student and Admin dashboards.
    Displays uploaded logo, user badge, navigation links, and logout.
    """
    def __init__(self, parent, user_data, nav_items, active_nav, on_nav_select, on_logout, **kwargs):
        super().__init__(parent, bg=COLOR_SIDEBAR, width=250, **kwargs)
        self.pack_propagate(False)
        self.user_data = user_data
        self.nav_items = nav_items
        self.active_nav = active_nav
        self.on_nav_select = on_nav_select
        self.on_logout = on_logout
        self.nav_buttons = {}

        self._build_sidebar()

    def _build_sidebar(self):
        # 1. Header & Logo
        header_frame = tk.Frame(self, bg=COLOR_SIDEBAR, padx=16, pady=18)
        header_frame.pack(fill="x")

        # Load Logo maintaining proportions, blended on sidebar background
        logo_photo = load_app_logo(max_width=218, max_height=56, bg_color=COLOR_SIDEBAR)
        if logo_photo:
            lbl_logo = tk.Label(header_frame, image=logo_photo, bg=COLOR_SIDEBAR)
            lbl_logo.image = logo_photo
            lbl_logo.pack(anchor="center", pady=(0, 6))

        # Tagline under header
        lbl_tag = tk.Label(
            header_frame,
            text=APP_TAGLINE,
            font=(FONT_FAMILY, 8, "italic"),
            fg="#95B5A5",
            bg=COLOR_SIDEBAR,
            anchor="center",
            justify="center",
            wraplength=218
        )
        lbl_tag.pack(fill="x")

        # Subtle divider
        sep = tk.Frame(self, bg="#214D3A", height=1)
        sep.pack(fill="x", padx=16, pady=(10, 12))

        # 2. User Profile Badge
        user_card = tk.Frame(self, bg="#123425", padx=12, pady=10)
        user_card.pack(fill="x", padx=14, pady=(0, 16))

        role_label = "Campus Administrator" if self.user_data.get("role") == "admin" else "Student"
        role_color = "#E9A23B" if self.user_data.get("role") == "admin" else "#67C293"

        lbl_role = tk.Label(
            user_card,
            text=f"● {role_label.upper()}",
            font=(FONT_FAMILY, 8, "bold"),
            fg=role_color,
            bg="#123425",
            anchor="w"
        )
        lbl_role.pack(fill="x")

        user_name = self.user_data.get("name", "User")
        lbl_name = tk.Label(
            user_card,
            text=user_name,
            font=(FONT_FAMILY, 10, "bold"),
            fg="#FFFFFF",
            bg="#123425",
            anchor="w"
        )
        lbl_name.pack(fill="x", pady=(2, 0))

        if self.user_data.get("role") == "student":
            reg_text = f"Reg: {self.user_data.get('reg_no', '')}"
            lbl_reg = tk.Label(
                user_card,
                text=reg_text,
                font=(FONT_FAMILY, 8),
                fg="#A3C2B1",
                bg="#123425",
                anchor="w"
            )
            lbl_reg.pack(fill="x")

        # 3. Navigation Buttons
        nav_container = tk.Frame(self, bg=COLOR_SIDEBAR)
        nav_container.pack(fill="both", expand=True, padx=10)

        for key, label in self.nav_items:
            is_active = (key == self.active_nav)
            btn = self._create_nav_button(nav_container, key, label, is_active)
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        # 4. Bottom Logout Button & Tagline
        bottom_frame = tk.Frame(self, bg=COLOR_SIDEBAR, padx=12, pady=16)
        bottom_frame.pack(side="bottom", fill="x")

        btn_logout = tk.Button(
            bottom_frame,
            text="🚪 Sign Out",
            command=self._confirm_logout,
            font=FONT_BODY_BOLD,
            bg="#214D3A",
            fg="#F7FAF8",
            activebackground="#D9534F",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=8
        )
        btn_logout.pack(fill="x")

        lbl_ver = tk.Label(
            bottom_frame,
            text=f"{APP_NAME} SRMIST v2.0",
            font=(FONT_FAMILY, 8),
            fg="#6B8E7D",
            bg=COLOR_SIDEBAR
        )
        lbl_ver.pack(pady=(8, 0))

    def _create_nav_button(self, parent, key, label, is_active):
        bg_col = "#238653" if is_active else COLOR_SIDEBAR
        fg_col = "#FFFFFF" if is_active else "#C4D6CC"
        font_style = FONT_BODY_BOLD if is_active else FONT_BODY

        btn = tk.Button(
            parent,
            text=f"  {label}",
            anchor="w",
            font=font_style,
            bg=bg_col,
            fg=fg_col,
            activebackground="#1E7548",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=9,
            command=lambda k=key: self.on_nav_select(k)
        )

        if not is_active:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1E5039", fg="#FFFFFF"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_SIDEBAR, fg="#C4D6CC"))

        return btn

    def _confirm_logout(self):
        res = messagebox.askyesno(
            "Confirm Sign Out",
            f"Are you sure you want to sign out of {APP_NAME}?",
            icon="question"
        )
        if res:
            self.on_logout()
