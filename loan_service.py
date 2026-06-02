import sqlite3
from datetime import date, timedelta


class BaseService:
    """
    Base service class for Library Certification App.
    Provides shared database connection logic for all services.
    """

    def __init__(self, db_name="library.db"):
        self.db_name = db_name

    def connect(self):
        """Create and return a database connection."""
        return sqlite3.connect(self.db_name)

    def validate(self, data: dict) -> bool:
        """
        Validate input data. Override in subclasses.

        Args:
            data: Dictionary of fields to validate.

        Returns:
            True if valid, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement validate()")


class LoanService(BaseService):
    """
    Service class for managing loan transactions.
    Inherits from BaseService (demonstrates inheritance).
    """

    def __init__(self, db_name="library.db"):
        super().__init__(db_name)

    def validate(self, data: dict) -> bool:
        """
        Validate loan input data (overrides BaseService).
        Demonstrates polymorphism — same method name, different behavior.

        Args:
            data: Must contain 'member_id' and 'collection_ids'.

        Returns:
            True if valid.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if not data.get("member_id"):
            raise ValueError("member_id is required.")
        if not data.get("collection_ids"):
            raise ValueError("At least one collection_id is required.")
        return True

    def calculate_due_date(self, borrow_date: date = None, days: int = 7) -> date:
        """
        Calculate the due date for a loan.

        Args:
            borrow_date: The date borrowing starts (defaults to today).
            days: Number of days until due (default 7).

        Returns:
            The calculated due date.
        """
        if borrow_date is None:
            borrow_date = date.today()
        return borrow_date + timedelta(days=days)

    def create_loan(self, member_id: int, collection_ids: list) -> int:
        """
        Create a new loan transaction.

        Args:
            member_id: The ID of the borrowing member.
            collection_ids: List of collection IDs being borrowed.

        Returns:
            The ID of the newly created loan.
        """
        self.validate({"member_id": member_id, "collection_ids": collection_ids})

        connection = self.connect()
        cursor = connection.cursor()

        borrow_date = date.today()
        due_date = self.calculate_due_date(borrow_date)

        cursor.execute(
            "INSERT INTO loans (member_id, borrow_date, due_date) VALUES (?, ?, ?)",
            (member_id, borrow_date.isoformat(), due_date.isoformat())
        )
        loan_id = cursor.lastrowid

        for collection_id in collection_ids:
            cursor.execute(
                "INSERT INTO loan_items (loan_id, collection_id) VALUES (?, ?)",
                (loan_id, collection_id)
            )
            cursor.execute(
                "UPDATE collections SET status = 'Borrowed' WHERE id = ?",
                (collection_id,)
            )

        connection.commit()
        connection.close()
        return loan_id

    def get_collection_status(self, collection_id: int) -> str:
        """
        Get the current status of a collection.

        Args:
            collection_id: The ID of the collection.

        Returns:
            Status string ('Available' or 'Borrowed').
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT status FROM collections WHERE id = ?",
            (collection_id,)
        )
        row = cursor.fetchone()
        connection.close()
        return row[0] if row else None

    def add_member(self, name: str, email: str, phone: str = "") -> int:
        """
        Add a new library member.

        Args:
            name: Member's full name.
            email: Member's email address.
            phone: Member's phone number (optional).

        Returns:
            The ID of the newly added member.
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        member_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return member_id

    def add_collection(self, title: str, author: str, category: str = "") -> int:
        """
        Add a new library collection/book.

        Args:
            title: Title of the collection.
            author: Author name.
            category: Collection category (optional).

        Returns:
            The ID of the newly added collection.
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO collections (title, author, category, status) VALUES (?, ?, ?, ?)",
            (title, author, category, "Available")
        )
        collection_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return collection_id