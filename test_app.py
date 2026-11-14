"""
test_app.py - Automated Verification and Headless UI Test Suite for UniResolve
Tests SRMIST validation, forgot password, custom locations, and GUI screen initialization.
"""

import sys
import unittest
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.dm = DataManager()
        self.dm._init_data()

    def test_authentication(self):
        # Admin authentication
        admin_user = self.dm.authenticate("admin", "admin123", "admin")
        self.assertIsNotNone(admin_user)
        self.assertEqual(admin_user["role"], "admin")

        # Student authentication
        stu_user = self.dm.authenticate("student1", "student123", "student")
        self.assertIsNotNone(stu_user)
        self.assertEqual(stu_user["name"], "Rahul Sharma")
        self.assertEqual(stu_user["reg_no"], "RA2511003010001")

        # Wrong password
        bad_pwd = self.dm.authenticate("student1", "wrongpwd", "student")
        self.assertIsNone(bad_pwd)

        # Wrong role
        bad_role = self.dm.authenticate("admin", "admin123", "student")
        self.assertIsNone(bad_role)

    def test_srmist_student_registration(self):
        # Valid SRMIST registration
        ok, msg = self.dm.register_student(
            name="Amit Kumar",
            reg_no="RA2511003010999",
            department="Computer Science & Engineering",
            year="1st Year",
            email="amit.kumar@srmist.edu.in",
            username="amit99",
            password="pass123"
        )
        self.assertTrue(ok, f"Registration failed unexpectedly: {msg}")
        self.assertIn("successful", msg.lower())

        # Invalid Email Domain (must be @srmist.edu.in)
        ok_bad_email, msg_bad_email = self.dm.register_student(
            name="Bad Email Student",
            reg_no="RA2511003010888",
            department="Computer Science & Engineering",
            year="1st Year",
            email="bad.student@gmail.com",
            username="bademail",
            password="pass123"
        )
        self.assertFalse(ok_bad_email)
        self.assertIn("@srmist.edu.in", msg_bad_email)

        # Invalid Registration Number Prefix (must start with RA25110)
        ok_bad_reg, msg_bad_reg = self.dm.register_student(
            name="Bad Reg Student",
            reg_no="REG2024099",
            department="Computer Science & Engineering",
            year="1st Year",
            email="bad.reg@srmist.edu.in",
            username="badreg",
            password="pass123"
        )
        self.assertFalse(ok_bad_reg)
        self.assertIn("RA25110", msg_bad_reg)

        # Non-digit suffix in registration number
        ok_non_digit, msg_non_digit = self.dm.register_student(
            name="Non Digit Student",
            reg_no="RA25110ABCDEF",
            department="Computer Science & Engineering",
            year="1st Year",
            email="nondigit@srmist.edu.in",
            username="nondigit",
            password="pass123"
        )
        self.assertFalse(ok_non_digit)
        self.assertIn("digits", msg_non_digit.lower())

        # Duplicate registration number
        ok_dup_reg, msg_dup_reg = self.dm.register_student(
            name="Duplicate Reg Student",
            reg_no="RA2511003010001",
            department="Information Technology",
            year="2nd Year",
            email="another@srmist.edu.in",
            username="anotheruser",
            password="pass123"
        )
        self.assertFalse(ok_dup_reg)
        self.assertIn("already registered", msg_dup_reg)

    def test_forgot_password_recovery(self):
        # 1. Verify existing student
        student = self.dm.verify_student_for_recovery(
            email="rahul.sharma@srmist.edu.in",
            reg_no="RA2511003010001"
        )
        self.assertIsNotNone(student)
        self.assertEqual(student["username"], "student1")

        # 2. Reset password
        ok, msg = self.dm.reset_password("student1", "newsecret2026")
        self.assertTrue(ok)

        # 3. Authenticate with new password
        auth_new = self.dm.authenticate("student1", "newsecret2026", "student")
        self.assertIsNotNone(auth_new)

        # 4. Old password should fail
        auth_old = self.dm.authenticate("student1", "student123", "student")
        self.assertIsNone(auth_old)

        # 5. Invalid recovery verification
        bad_student = self.dm.verify_student_for_recovery("wrong@srmist.edu.in", "RA2511003010001")
        self.assertIsNone(bad_student)

    def test_campus_locations_and_custom_addition(self):
        # Verify 6 required predefined locations
        required_locations = [
            "TP1",
            "TP2",
            "JAVA CANTEEN",
            "UNIVERSITY BUILDING",
            "TP GANESHAN",
            "VENDHAR SQUARE"
        ]
        for loc in required_locations:
            self.assertIn(loc, self.dm.locations)

        # Add custom location
        ok, res = self.dm.add_custom_location("Biotech Block 3rd Floor")
        self.assertTrue(ok)
        self.assertEqual(res, "BIOTECH BLOCK 3RD FLOOR")
        self.assertIn("BIOTECH BLOCK 3RD FLOOR", self.dm.locations)

    def test_complaint_addition_and_custom_location_stored(self):
        initial_count = len(self.dm.get_all_complaints())
        new_c, msg = self.dm.add_complaint(
            student_username="student1",
            title="Lab PC Screen Flickering",
            category="IT & Network",
            location="TP1",
            priority="High",
            description="System #14 monitor exhibits high-frequency flickering in Lab 2."
        )
        self.assertIsNotNone(new_c)
        self.assertEqual(new_c["id"], "CMP006")
        self.assertEqual(new_c["status"], "Pending")
        self.assertEqual(new_c["location"], "TP1")
        self.assertEqual(len(self.dm.get_all_complaints()), initial_count + 1)

class TestUIInitialization(unittest.TestCase):
    def test_ui_screens_creation(self):
        import tkinter as tk
        from main import UniResolveApp
        from views.login_view import LoginView
        from views.register_view import RegisterView
        from views.student_dashboard import StudentDashboardView
        from views.submit_complaint import SubmitComplaintView
        from views.my_complaints import MyComplaintsView
        from views.admin_dashboard import AdminDashboardView
        from views.admin_manage import AdminManageView
        from views.help_view import HelpView
        from views.details_dialog import ComplaintDetailsDialog
        from views.forgot_password_dialog import ForgotPasswordDialog

        app = UniResolveApp()
        app.withdraw()  # Hide window during test

        # 1. Test Login View
        app.show_login()
        app.update_idletasks()

        # 2. Test Forgot Password Dialog
        fp_dlg = ForgotPasswordDialog(app, on_recovery_success=lambda u: None)
        fp_dlg.update_idletasks()
        fp_dlg.destroy()

        # 3. Test Register View
        app.show_register()
        app.update_idletasks()

        # 4. Test Student Dashboard & student views
        dm = DataManager()
        student = dm.get_student("student1")
        app.on_login_success(student)
        app.update_idletasks()

        # Navigate through all student screens
        app.navigate_to_screen("dashboard")
        app.update_idletasks()
        app.navigate_to_screen("submit_complaint")
        app.update_idletasks()
        app.navigate_to_screen("my_complaints")
        app.update_idletasks()
        app.navigate_to_screen("help")
        app.update_idletasks()

        # 5. Test Admin flow
        admin = dm.authenticate("admin", "admin123", "admin")
        app.on_login_success(admin)
        app.update_idletasks()

        app.navigate_to_screen("dashboard")
        app.update_idletasks()
        app.navigate_to_screen("manage_complaints")
        app.update_idletasks()
        app.navigate_to_screen("help")
        app.update_idletasks()

        # 6. Test Details Dialog instantiation
        dlg = ComplaintDetailsDialog(app, "CMP001", is_admin=True)
        dlg.update_idletasks()
        dlg.destroy()

        app.destroy()
        print("All UniResolve UI Screens and Workflows initialized successfully!")

if __name__ == "__main__":
    unittest.main()
