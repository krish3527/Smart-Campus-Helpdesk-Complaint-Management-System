"""
test_workflow.py - End-to-End User Story Workflow Test for UniResolve
Simulates:
Student Login -> Submit Complaint (with SRMIST Location) -> Auto ID -> Admin Login -> View -> Update Status -> Student checks updated status
"""

import unittest
from data_manager import DataManager

class TestWorkflow(unittest.TestCase):
    def test_full_user_story(self):
        dm = DataManager()
        dm._init_data()

        # Step 1: Student logs in
        student = dm.authenticate("student1", "student123", "student")
        self.assertIsNotNone(student, "Student authentication failed")
        initial_stats = dm.get_stats_for_student("student1")
        self.assertEqual(initial_stats["total"], 3)
        self.assertEqual(initial_stats["pending"], 1)

        # Step 2: Student submits complaint at TP1
        new_c, msg = dm.add_complaint(
            student_username="student1",
            title="Broken Laboratory Chair",
            category="Classroom & Laboratory",
            location="TP1",
            priority="Medium",
            description="Left armrest and back support cracked on lab stool #12."
        )
        self.assertIsNotNone(new_c, f"Submission failed: {msg}")
        cid = new_c["id"]
        self.assertEqual(cid, "CMP006")
        self.assertEqual(new_c["status"], "Pending")
        self.assertEqual(new_c["location"], "TP1")

        # Step 3: Verify Student Dashboard stats immediately reflect submission
        updated_stats = dm.get_stats_for_student("student1")
        self.assertEqual(updated_stats["total"], 4)
        self.assertEqual(updated_stats["pending"], 2)

        # Step 4: Admin logs in
        admin = dm.authenticate("admin", "admin123", "admin")
        self.assertIsNotNone(admin, "Admin authentication failed")

        # Step 5: Admin views all complaints and finds CMP006
        found = dm.get_complaint_by_id(cid)
        self.assertIsNotNone(found)
        self.assertEqual(found["title"], "Broken Laboratory Chair")
        self.assertEqual(found["status"], "Pending")

        # Step 6: Admin updates status to 'In Progress'
        ok, update_msg = dm.update_complaint_status(cid, "In Progress", "Carpentry technician assigned at TP1.")
        self.assertTrue(ok)
        self.assertEqual(dm.get_complaint_by_id(cid)["status"], "In Progress")

        # Step 7: Admin updates status to 'Resolved'
        ok, update_msg = dm.update_complaint_status(cid, "Resolved", "Welded and repaired. Safe for student use.")
        self.assertTrue(ok)
        self.assertEqual(dm.get_complaint_by_id(cid)["status"], "Resolved")

        # Step 8: Student checks updated status
        student_complaints = dm.get_complaints_by_student("student1")
        my_c = next(c for c in student_complaints if c["id"] == cid)
        self.assertEqual(my_c["status"], "Resolved")
        self.assertEqual(my_c["admin_remarks"], "Welded and repaired. Safe for student use.")

        final_stats = dm.get_stats_for_student("student1")
        self.assertEqual(final_stats["total"], 4)
        self.assertEqual(final_stats["pending"], 1)
        self.assertEqual(final_stats["resolved"], 2)

        print(f"UniResolve End-to-End Workflow passed! Ticket {cid} successfully moved from Pending -> In Progress -> Resolved.")

if __name__ == "__main__":
    unittest.main()
