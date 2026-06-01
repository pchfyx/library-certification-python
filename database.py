import sqlite3
from datetime import date, timedelta


class Database:
    """
    Database class for Library Certification App.
    This class handles the SQLite database connection and all database tables.
    """

    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        """Create and return database connection."""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Create required database tables if they do not exist."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT,
                status TEXT NOT NULL DEFAULT 'Available'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loan_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_id INTEGER NOT NULL,
                collection_id INTEGER NOT NULL,
                FOREIGN KEY (loan_id) REFERENCES loans(id),
                FOREIGN KEY (collection_id) REFERENCES collections(id)
            )
        """)

        connection.commit()
        connection.close()

    def add_member(self, name, email, phone):
        """Add new library member."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO members (name, email, phone)
            VALUES (?, ?, ?)
        """, (name, email, phone))

        connection.commit()
        connection.close()

    def get_members(self):
        """Get all members."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()

        connection.close()
        return members

    def add_collection(self, title, author, category):
        """Add new library collection/book."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO collections (title, author, category, status)
            VALUES (?, ?, ?, ?)
        """, (title, author, category, "Available"))

        connection.commit()
        connection.close()

    def get_collections(self):
        """Get all library collections/books."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM collections")
        collections = cursor.fetchall()

        connection.close()
        return collections

    def create_loan(self, member_id, collection_ids):
        """
        Create a loan transaction.
        Due date is automatically 7 days after borrow date.
        """
        connection = self.connect()
        cursor = connection.cursor()

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=7)

        cursor.execute("""
            INSERT INTO loans (member_id, borrow_date, due_date)
            VALUES (?, ?, ?)
        """, (member_id, borrow_date.isoformat(), due_date.isoformat()))

        loan_id = cursor.lastrowid

        for collection_id in collection_ids:
            cursor.execute("""
                INSERT INTO loan_items (loan_id, collection_id)
                VALUES (?, ?)
            """, (loan_id, collection_id))

            cursor.execute("""
                UPDATE collections
                SET status = 'Borrowed'
                WHERE id = ?
            """, (collection_id,))

        connection.commit()
        connection.close()

        return loan_id

    def get_loans(self):
        """Get loan history with member and collection information."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                loans.id,
                members.name,
                collections.title,
                loans.borrow_date,
                loans.due_date
            FROM loans
            JOIN members ON loans.member_id = members.id
            JOIN loan_items ON loans.id = loan_items.loan_id
            JOIN collections ON loan_items.collection_id = collections.id
            ORDER BY loans.id DESC
        """)

        loans = cursor.fetchall()

        connection.close()
        return loans