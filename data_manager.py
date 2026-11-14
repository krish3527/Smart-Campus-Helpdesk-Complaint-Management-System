"""
data_manager.py - In-Memory Data Store for UniResolve
Campus Helpdesk & Complaint Management System
Manages SRMIST students, facility administrators, complaints,
sample records, and shared session operations.
"""

from datetime import datetime

class DataManager:
    _instance = None

    def __new__(cls):
        # Singleton pattern to ensure all views share the exact same in-memory data
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._init_data()
        return cls._instance

    def _init_data(self):
        # Sample Facility Administrators
        self.admins = {
            "admin": {
                "username": "admin",
                "password": "admin123",
                "name": "Campus Administrator",
                "role": "admin",
                "email": "admin@srmist.edu.in",
                "department": "Campus Facility Management"
            }
        }

        # Sample Registered SRMIST Students (using RA25110 format & @srmist.edu.in)
        self.students = {
            "student1": {
                "username": "student1",
                "password": "student123",
                "name": "Rahul Sharma",
                "reg_no": "RA2511003010001",
                "department": "Computer Science",
                "year": "3rd Year",
                "email": "rahul.sharma@srmist.edu.in",
                "role": "student"
            },
            "student2": {
                "username": "student2",
                "password": "student123",
                "name": "Priya Patel",
                "reg_no": "RA2511003010045",
                "department": "Electronics & Communication",
                "year": "2nd Year",
                "email": "priya.patel@srmist.edu.in",
                "role": "student"
            }
        }

        # Complaint Categories
        self.categories = [
            "Infrastructure",
            "Electrical",
            "IT & Network",
            "Cleanliness",
            "Classroom & Laboratory"
        ]

        # SRMIST Campus Locations (as specified in requirement 4)
        self.locations = [
            "TP1",
            "TP2",
            "JAVA CANTEEN",
            "UNIVERSITY BUILDING",
            "TP GANESHAN",
            "VENDHAR SQUARE"
        ]

        # Priority levels
        self.priorities = ["Low", "Medium", "High"]

        # Statuses
        self.statuses = ["Pending", "In Progress", "Resolved"]

        # Preloaded Sample Complaints
        self.complaints = [
            {
                "id": "CMP001",
                "student_username": "student1",
                "student_name": "Rahul Sharma",
                "student_reg": "RA2511003010001",
                "student_dept": "Computer Science",
                "title": "Projector Not Working",
                "category": "Classroom & Laboratory",
                "location": "UNIVERSITY BUILDING",
                "priority": "High",
                "status": "Pending",
                "date": "2026-11-10",
                "description": "The ceiling projector in UB Room 402 fails to power on during morning lectures. HDMI and power connections checked. Urgent replacement required.",
                "admin_remarks": "Assigned to AV facility team for inspection."
            },
            {
                "id": "CMP002",
                "student_username": "student1",
                "student_name": "Rahul Sharma",
                "student_reg": "RA2511003010001",
                "student_dept": "Computer Science",
                "title": "Wi-Fi Connectivity Issue",
                "category": "IT & Network",
                "location": "TP1",
                "priority": "Medium",
                "status": "In Progress",
                "date": "2026-11-11",
                "description": "Frequent connection drops on student Wi-Fi network 'SRM-Student-5G' inside Tech Park 1, 3rd floor computer laboratory.",
                "admin_remarks": "IT network team verified signal strength. Replacement access point scheduled for installation."
            },
            {
                "id": "CMP003",
                "student_username": "student2",
                "student_name": "Priya Patel",
                "student_reg": "RA2511003010045",
                "student_dept": "Electronics & Communication",
                "title": "Broken Classroom Fan",
                "category": "Electrical",
                "location": "TP2",
                "priority": "High",
                "status": "Resolved",
                "date": "2026-11-08",
                "description": "Ceiling fan #2 in Classroom TP2-205 is not rotating and emits a buzzing sound when switched on. Potential electrical hazard.",
                "admin_remarks": "Maintenance team replaced the motor capacitor and lubricated bearings on 2026-11-09. Verified fully operational."
            },
            {
                "id": "CMP004",
                "student_username": "student2",
                "student_name": "Priya Patel",
                "student_reg": "RA2511003010045",
                "student_dept": "Electronics & Communication",
                "title": "Washroom Cleaning Required",
                "category": "Cleanliness",
                "location": "JAVA CANTEEN",
                "priority": "Medium",
                "status": "Pending",
                "date": "2026-11-12",
                "description": "Ground floor washroom near Java Canteen requires deep cleaning and liquid soap dispenser refill.",
                "admin_remarks": ""
            },
            {
                "id": "CMP005",
                "student_username": "student1",
                "student_name": "Rahul Sharma",
                "student_reg": "RA2511003010001",
                "student_dept": "Computer Science",
                "title": "Damaged Classroom Desk",
                "category": "Infrastructure",
                "location": "TP GANESHAN",
                "priority": "Low",
                "status": "Resolved",
                "date": "2026-11-05",
                "description": "Wooden bench in row 4 of TP Ganeshan Auditorium annex has a loose armrest with protruding screws.",
                "admin_remarks": "Carpentry section repaired desk top, replaced screws, and revarnished surface."
            }
        ]

    # --- Validation Helpers ---

    @staticmethod
    def validate_srmist_email(email):
        """
        Validates that email strictly belongs to the SRMIST domain: @srmist.edu.in
        """
        email = email.strip().lower()
        domain = "@srmist.edu.in"
        if not email.endswith(domain):
            return False, "Registration is restricted to SRMIST students. Email must end with @srmist.edu.in (e.g. student@srmist.edu.in)."
        prefix = email[:-len(domain)]
        if not prefix:
            return False, "Please enter your student username or ID before @srmist.edu.in."
        return True, ""

    @staticmethod
    def validate_srmist_reg_no(reg_no):
        """
        Validates that registration number starts with RA25110 followed by digits.
        """
        reg = reg_no.strip().upper()
        prefix = "RA25110"
        if not reg.startswith(prefix):
            return False, "Registration Number must start with the SRMIST prefix 'RA25110' (e.g. RA2511000000)."
        suffix = reg[len(prefix):]
        if not suffix or not suffix.isdigit():
            return False, "Registration Number must consist of 'RA25110' followed strictly by digits (e.g. RA2511003010001)."
        return True, ""

    # --- Authentication Methods ---

    def authenticate(self, username, password, role):
        """
        Authenticate user with username, password, and chosen role.
        Returns user dictionary if credentials match, else None.
        """
        username = username.strip().lower()
        password = password.strip()

        if role.lower() == "admin":
            user = self.admins.get(username)
            if user and user["password"] == password:
                return user
        elif role.lower() == "student":
            user = self.students.get(username)
            if user and user["password"] == password:
                return user
        return None

    def register_student(self, name, reg_no, department, year, email, username, password):
        """
        Register a new student in the system with SRMIST specific validation.
        """
        name = name.strip()
        reg_no = reg_no.strip().upper()
        department = department.strip()
        year = year.strip()
        email = email.strip().lower()
        username = username.strip().lower()
        password = password.strip()

        # Check for empty fields
        if not all([name, reg_no, department, year, email, username, password]):
            return False, "All fields marked with * are required. Please fill in every field."

        if len(name) < 2:
            return False, "Please enter your full legal name."

        # SRMIST Registration Number Validation
        is_valid_reg, reg_err = self.validate_srmist_reg_no(reg_no)
        if not is_valid_reg:
            return False, reg_err

        # SRMIST Email Validation
        is_valid_email, email_err = self.validate_srmist_email(email)
        if not is_valid_email:
            return False, email_err

        if len(username) < 3:
            return False, "Username must be at least 3 characters long."

        if len(password) < 4:
            return False, "Password must be at least 4 characters long."

        # Unique username check
        if username in self.students or username in self.admins:
            return False, f"Username '{username}' is already taken. Please choose another username."

        # Unique registration number check
        for student in self.students.values():
            if student["reg_no"] == reg_no:
                return False, f"Registration number '{reg_no}' is already registered in UniResolve."

        # Unique email check among students
        for student in self.students.values():
            if student["email"] == email:
                return False, f"Email '{email}' is already registered in the system."

        # Save student record
        self.students[username] = {
            "username": username,
            "password": password,
            "name": name,
            "reg_no": reg_no,
            "department": department,
            "year": year,
            "email": email,
            "role": "student"
        }
        return True, "Registration successful! You can now log in with your credentials."

    def get_student(self, username):
        """Retrieve student record by username."""
        return self.students.get(username.strip().lower())

    # --- Password Recovery (Forgot Password) ---

    def verify_student_for_recovery(self, email, reg_no):
        """
        Verify that an email and registration number belong to an existing student.
        Returns student dictionary if verified, else None.
        """
        email = email.strip().lower()
        reg_no = reg_no.strip().upper()

        for student in self.students.values():
            if student["email"] == email and student["reg_no"] == reg_no:
                return student
        return None

    def reset_password(self, username, new_password):
        """
        Update the student's password in memory.
        """
        username = username.strip().lower()
        new_password = new_password.strip()

        if len(new_password) < 4:
            return False, "New password must be at least 4 characters long."

        if username in self.students:
            self.students[username]["password"] = new_password
            return True, "Password has been updated successfully! You can now log in."
        return False, "User account not found."

    # --- Campus Location Management ---

    def add_custom_location(self, loc_name):
        """
        Adds a custom campus location entered by a student.
        Keeps predefined locations available.
        """
        loc_name = loc_name.strip().upper()
        if not loc_name:
            return False, "Custom location cannot be empty."

        for existing in self.locations:
            if existing.upper() == loc_name:
                return True, existing

        self.locations.append(loc_name)
        return True, loc_name

    # --- Complaint Management Methods ---

    def _generate_complaint_id(self):
        """Generate unique next complaint ID (e.g., CMP006)."""
        existing_nums = []
        for c in self.complaints:
            cid = c.get("id", "")
            if cid.startswith("CMP"):
                try:
                    num = int(cid[3:])
                    existing_nums.append(num)
                except ValueError:
                    pass
        next_num = max(existing_nums, default=0) + 1
        return f"CMP{next_num:03d}"

    def add_complaint(self, student_username, title, category, location, priority, description):
        """
        Create and record a new complaint from a student.
        """
        student = self.get_student(student_username)
        if not student:
            return None, "Student record not found."

        title = title.strip()
        location = location.strip()
        description = description.strip()

        if not title:
            return None, "Complaint Title cannot be empty."
        if not category:
            return None, "Please select a Category."
        if not location:
            return None, "Please specify a Campus Location."
        if not priority:
            return None, "Please choose a Priority level."
        if not description:
            return None, "Please provide a detailed Description of the issue."

        new_id = self._generate_complaint_id()
        current_date = datetime.now().strftime("%Y-%m-%d")

        new_complaint = {
            "id": new_id,
            "student_username": student["username"],
            "student_name": student["name"],
            "student_reg": student["reg_no"],
            "student_dept": student["department"],
            "title": title,
            "category": category,
            "location": location,
            "priority": priority,
            "status": "Pending",
            "date": current_date,
            "description": description,
            "admin_remarks": ""
        }

        # Insert at top so newest appears first
        self.complaints.insert(0, new_complaint)
        return new_complaint, f"Complaint {new_id} submitted successfully!"

    def get_all_complaints(self):
        """Return all complaints."""
        return self.complaints

    def get_complaints_by_student(self, username):
        """Return all complaints submitted by a particular student."""
        username = username.strip().lower()
        return [c for c in self.complaints if c["student_username"] == username]

    def get_complaint_by_id(self, complaint_id):
        """Find a complaint by its ID."""
        complaint_id = complaint_id.strip().upper()
        for c in self.complaints:
            if c["id"].upper() == complaint_id:
                return c
        return None

    def update_complaint_status(self, complaint_id, new_status, remarks=None):
        """
        Update the status and optional admin remarks of a complaint.
        """
        complaint = self.get_complaint_by_id(complaint_id)
        if not complaint:
            return False, f"Complaint {complaint_id} not found."

        if new_status not in self.statuses:
            return False, f"Invalid status: {new_status}"

        complaint["status"] = new_status
        if remarks is not None:
            complaint["admin_remarks"] = remarks.strip()

        return True, f"Complaint {complaint_id} status updated to '{new_status}' successfully."

    # --- Statistics Methods ---

    def get_stats_for_student(self, username):
        """Compute summary statistics for student dashboard."""
        student_complaints = self.get_complaints_by_student(username)
        total = len(student_complaints)
        pending = sum(1 for c in student_complaints if c["status"] == "Pending")
        in_progress = sum(1 for c in student_complaints if c["status"] == "In Progress")
        resolved = sum(1 for c in student_complaints if c["status"] == "Resolved")
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "resolved": resolved
        }

    def get_stats_for_admin(self):
        """Compute overall campus statistics for administrator dashboard."""
        total = len(self.complaints)
        pending = sum(1 for c in self.complaints if c["status"] == "Pending")
        in_progress = sum(1 for c in self.complaints if c["status"] == "In Progress")
        resolved = sum(1 for c in self.complaints if c["status"] == "Resolved")

        # Category breakdown
        category_counts = {cat: 0 for cat in self.categories}
        for c in self.complaints:
            cat = c.get("category", "")
            if cat in category_counts:
                category_counts[cat] += 1
            else:
                category_counts[cat] = 1

        # Priority breakdown
        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        for c in self.complaints:
            p = c.get("priority", "Low")
            if p in priority_counts:
                priority_counts[p] += 1

        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "resolved": resolved,
            "categories": category_counts,
            "priorities": priority_counts
        }

    # --- Filtering and Search ---

    def filter_complaints(self, complaints_list, search_query="", category="All", status="All", priority="All"):
        """
        Filter a given list of complaints based on search query and criteria.
        """
        filtered = complaints_list

        if search_query:
            query = search_query.strip().lower()
            filtered = [
                c for c in filtered
                if (query in c["id"].lower() or
                    query in c["title"].lower() or
                    query in c["student_name"].lower() or
                    query in c["location"].lower())
            ]

        if category and category != "All":
            filtered = [c for c in filtered if c["category"] == category]

        if status and status != "All":
            filtered = [c for c in filtered if c["status"] == status]

        if priority and priority != "All":
            filtered = [c for c in filtered if c["priority"] == priority]

        return filtered
