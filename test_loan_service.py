import unittest
import os
import sqlite3
from datetime import date, timedelta

from database import Database


class TestLibraryDatabase(unittest.TestCase):
    """
    Unit tests for Library Certification App.
    These tests validate database operations and borrowing logic.
    """

    def setUp(self):
        """
        Prepare a temporary test database before each test.
        This prevents testing from changing the real library.db file.
        """
        self.test_db_name = "test_library.db"
        self.db = Database(self.test_db_name)

    def tearDown(self):
        """
        Delete the temporary test database after each test.
        """
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)

    def test_add_member(self):
        """
        Test that a member can be added to the database.
        """
        self.db.add_member("Alice", "alice@example.com", "0811111111")
        members = self.db.get_members()

        self.assertEqual(len(members), 1)
        self.assertEqual(members[0][1], "Alice")
        self.assertEqual(members[0][2], "alice@example.com")

    def test_add_collection(self):
        """
        Test that a library collection/book can be added to the database.
        """
        self.db.add_collection("Clean Code", "Robert C. Martin", "Programming")
        collections = self.db.get_collections()

        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0][1], "Clean Code")
        self.assertEqual(collections[0][4], "Available")

    def test_create_loan(self):
        """
        Test that a borrowing transaction can be created.
        """
        self.db.add_member("Bob", "bob@example.com", "0822222222")
        self.db.add_collection("Python Basics", "John Smith", "Programming")

        loan_id = self.db.create_loan(1, [1])
        loans = self.db.get_loans()

        self.assertEqual(loan_id, 1)
        self.assertEqual(len(loans), 1)
        self.assertEqual(loans[0][1], "Bob")
        self.assertEqual(loans[0][2], "Python Basics")

    def test_due_date_is_7_days_after_borrow_date(self):
        """
        Test that due date is automatically 7 days after borrow date.
        This matches the library borrowing requirement.
        """
        self.db.add_member("Charlie", "charlie@example.com", "0833333333")
        self.db.add_collection("Database System", "Jane Doe", "Database")

        self.db.create_loan(1, [1])
        loans = self.db.get_loans()

        expected_borrow_date = date.today().isoformat()
        expected_due_date = (date.today() + timedelta(days=7)).isoformat()

        self.assertEqual(loans[0][3], expected_borrow_date)
        self.assertEqual(loans[0][4], expected_due_date)

    def test_collection_status_changes_to_borrowed(self):
        """
        Test that a collection status changes to Borrowed after loan is created.
        """
        self.db.add_member("David", "david@example.com", "0844444444")
        self.db.add_collection("Software Engineering", "Ian Sommerville", "Software")

        self.db.create_loan(1, [1])
        collections = self.db.get_collections()

        self.assertEqual(collections[0][4], "Borrowed")


if __name__ == "__main__":
    unittest.main()