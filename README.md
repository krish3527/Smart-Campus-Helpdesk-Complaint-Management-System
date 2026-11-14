# UniResolve – Campus Helpdesk & Complaint Management System

> **"Your Campus. Your Voice. Our Resolution."**

A college desktop GUI application built using **Python and Tkinter** for SRMIST students and campus administrators to report, manage, and resolve facility issues.

---

## 📌 Project Overview

**UniResolve** provides a structured digital platform tailored for SRMIST campus operations:
1. **Students**: Register with their official SRMIST email (`@srmist.edu.in`) and registration number (`RA25110...`), submit campus complaints across SRMIST locations (TP1, TP2, Java Canteen, UB, TP Ganeshan, Vendhar Square, or custom spots), recover forgotten passwords, and track real-time resolution updates.
2. **Administrators**: Access an administrative console to inspect tickets, filter by department/category, review problem descriptions, and update resolution statuses (`Pending` ➔ `In Progress` ➔ `Resolved`) with technician remarks.

---

## 🛠️ Technology Stack

- **Language**: Python 3.8+ (Tested on Python 3.11)
- **GUI Framework**: Tkinter & `ttk` (Themed Tkinter)
- **Styling**: Custom Tkinter color schemes, high-DPI scaling, and modern treeviews
- **Image Processing**: Pillow (`PIL`) for aspect-ratio-preserving logo display
- **Data Persistence**: In-memory Python data store (lists & dictionaries) with singleton architecture

---

## 🎨 Design Theme & Colors

UniResolve strictly adheres to a clean academic green-and-white color palette:
- **Sidebar**: `#173D2D` (Deep Forest Green)
- **Primary Brand Green**: `#238653` (Vibrant Campus Green)
- **Background**: `#F4F7F5` (Soft Off-White)
- **Cards**: `#FFFFFF` (Pure White)
- **Main Headings/Text**: `#26352C` (Dark Slate Green)
- **Muted Subtext**: `#78857D` (Subtle Gray-Green)
- **Pending Status**: `#E9A23B` (Warm Amber)
- **In Progress Status**: `#397CC5` (Executive Blue)
- **Resolved Status**: `#238653` (Success Green)
- **High Priority**: `#D9534F` (Soft Crimson)

---

## 📂 Project Structure

```
Smart-Campus-Helpdesk-Complaint-Management-System/
│
├── main.py                    # Application entry point, window management & navigation router
├── data_manager.py            # In-memory data store, auth, validation, sample complaints & filters
├── ui_components.py           # Custom styled widgets (Stat cards, buttons, treeviews, sidebar, logo loader)
├── requirements.txt           # Python dependencies (Pillow)
├── README.md                  # Complete documentation and viva guide
├── test_app.py                # Automated unit and GUI initialization test suite
├── test_workflow.py           # End-to-end user story simulation test
│
├── views/
│   ├── __init__.py
│   ├── login_view.py          # Screen 1: Login Page with Forgot Password & demo auto-fill
│   ├── register_view.py       # Screen 2: Student Registration (RA25110 & @srmist.edu.in validation)
│   ├── forgot_password_dialog.py # Screen: Forgot Password recovery dialog
│   ├── student_dashboard.py   # Screen 3: Student Dashboard with 4 stat cards & recent complaints
│   ├── submit_complaint.py    # Screen 4: Submit Complaint form (SRMIST locations & Custom Location popup)
│   ├── my_complaints.py       # Screen 5: My Complaints table with search, filters & details
│   ├── admin_dashboard.py     # Screen 6: Administrator Dashboard with category breakdown
│   ├── admin_manage.py        # Screen 7: Manage Complaints with status updates & remarks
│   ├── help_view.py           # Screen 8: Help & FAQ with SRMIST helpdesk contact cards
│   └── details_dialog.py      # Modal popup for inspecting & resolving tickets
│
└── assets/
    ├── logo.png               # Uploaded SRMIST Resolve official logo (788x184 RGBA)
    └── logo_crest.png         # SRMIST crest icon for taskbar / window icon
```

---

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure Python 3 is installed. You can check via:
```bash
python --version
```

### 2. Install Dependencies
Install Pillow for logo and image rendering:
```bash
pip install -r requirements.txt
```

### 3. Launch UniResolve
Run the application:
```bash
python main.py
```

---

## 🔑 Preloaded Demo Credentials

For quick viva evaluation and project demonstration, the login screen includes **Quick Demo Auto-Fill Buttons** that populate credentials with a single click.

| Role | Username | Password | Full Name | Registration Number | Email |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Campus Administrator | - | `admin@srmist.edu.in` |
| **Student 1** | `student1` | `student123` | Rahul Sharma | `RA2511003010001` | `rahul.sharma@srmist.edu.in` |
| **Student 2** | `student2` | `student123` | Priya Patel | `RA2511003010045` | `priya.patel@srmist.edu.in` |

---

## 📋 Predefined SRMIST Locations

1. **TP1** (Tech Park 1)
2. **TP2** (Tech Park 2)
3. **JAVA CANTEEN**
4. **UNIVERSITY BUILDING**
5. **TP GANESHAN** (Auditorium & Annex)
6. **VENDHAR SQUARE**
7. **+ Custom Location**: Click the `➕ Custom Location` button to add any campus building, lab, or floor. The custom location is stored with the complaint and remains selectable in the dropdown.

---

## 🔐 SRMIST Format Requirements

- **Registration Number**: Must begin with `RA25110` followed strictly by digits (e.g. `RA2511003010001`). Non-matching formats are rejected with a clear validation popup.
- **Email Address**: Must belong to the `@srmist.edu.in` domain (e.g. `student@srmist.edu.in`).
- **Forgot Password**: Allows students to reset their password locally by verifying their registered `@srmist.edu.in` email and `RA25110...` registration number without external email APIs.

---

## 🔄 Complete Demonstration Walkthrough (Viva Demo)

Follow these steps to demonstrate the full application workflow:

1. **Launch**: Run `python main.py`. Observe the official SRMIST **UniResolve** logo and the tagline: *"Your Campus. Your Voice. Our Resolution."*
2. **Student Login**: Click **Student (student1)** auto-fill button, then click **Sign In to UniResolve**.
3. **Student Dashboard**: Observe the welcome banner, the 4 summary stat cards (`Total: 3`, `Pending: 1`, `In Progress: 1`, `Resolved: 1`), and the recent complaints table.
4. **Submit New Complaint**:
   - Click the green **➕ Submit New Complaint** button.
   - Enter Title: `Computer Lab AC Leaking Water`.
   - Category: `Electrical`.
   - Location: Choose `TP1` or click **➕ Custom Location** to add `Biotech Block 3rd Floor`.
   - Priority: `High`.
   - Description: `AC unit #3 on the east wall is dripping water directly above workbench 4.`
   - Click **✓ Submit Complaint to UniResolve**.
   - A success popup appears with Ticket ID **`CMP006`**.
5. **Check My Complaints**:
   - The app redirects to the **My Complaints** table.
   - Notice `CMP006` is listed with a warm amber `● Pending` status.
   - Double-click the record to open the **Complaint Record Details** modal.
6. **Sign Out**: Click **🚪 Sign Out** on the sidebar and confirm.
7. **Forgot Password Demo**:
   - On the login screen, click **Forgot Password?**.
   - Enter Email: `rahul.sharma@srmist.edu.in` and Reg No: `RA2511003010001`.
   - Click **Verify Credentials**. The dialog verifies the student and unlocks the password reset form.
   - Enter a new password: `mypassword2026`, confirm it, and click **Update Password**.
   - Notice the success message and automatic redirect to the login screen with username pre-filled!
8. **Admin Login**:
   - Click **Admin (admin)** auto-fill, then click **Sign In**.
9. **Admin Manage Complaints**:
   - Click **⚙️ All Complaints** in the sidebar.
   - Locate ticket `CMP006`.
   - Double-click `CMP006` to open the full modal. Change status to **`Resolved`**, type resolution notes: `Technician cleared the drain pipe and tested condenser. Working normally.`, then click **💾 Save Status & Remarks**.
10. **Verify Real-time Cross-Role Reflection**:
    - Sign out of admin.
    - Log back in as `student1` (using the updated password).
    - Go to **My Complaints**: `CMP006` now displays a green `● Resolved` tag and the student can see the administrator's resolution remarks!

---

## 🧪 Automated Testing

Both automated unit tests and user story workflow tests are included:
```bash
# Run unit & screen initialization tests
python test_app.py

# Run end-to-end user workflow simulation test
python test_workflow.py
```

---

## 📄 License
Developed for academic demonstration, student mini-projects, and college viva presentations at SRMIST.
