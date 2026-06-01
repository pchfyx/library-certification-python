import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from report_generator import ReportGenerator


class LibraryApp:
    """
    Main desktop application for Library Certification App.
    This class handles the user interface using Tkinter.
    """

    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Library Certification App")
        self.root.geometry("900x600")

        self.create_tabs()

    def create_tabs(self):
        """Create main application tabs."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.catalog_tab = ttk.Frame(notebook)
        self.member_tab = ttk.Frame(notebook)
        self.collection_tab = ttk.Frame(notebook)
        self.loan_tab = ttk.Frame(notebook)
        self.history_tab = ttk.Frame(notebook)

        notebook.add(self.catalog_tab, text="Catalog")
        notebook.add(self.member_tab, text="Members")
        notebook.add(self.collection_tab, text="Collections")
        notebook.add(self.loan_tab, text="Borrowing")
        notebook.add(self.history_tab, text="Loan History")

        self.create_catalog_tab()
        self.create_member_tab()
        self.create_collection_tab()
        self.create_loan_tab()
        self.create_history_tab()

    # =========================
    # Catalog Tab
    # =========================

    def create_catalog_tab(self):
        """Create catalog page for displaying all collections."""
        ttk.Label(
            self.catalog_tab,
            text="Library Catalog",
            font=("Arial", 16)
        ).pack(pady=10)

        self.catalog_tree = ttk.Treeview(
            self.catalog_tab,
            columns=("ID", "Title", "Author", "Category", "Status"),
            show="headings"
        )

        for col in ("ID", "Title", "Author", "Category", "Status"):
            self.catalog_tree.heading(col, text=col)

        self.catalog_tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(
            self.catalog_tab,
            text="Refresh Catalog",
            command=self.load_catalog
        ).pack(pady=10)

        self.load_catalog()

    # =========================
    # Member Tab
    # =========================

    def create_member_tab(self):
        """Create member management page."""
        ttk.Label(
            self.member_tab,
            text="Add Library Member",
            font=("Arial", 16)
        ).pack(pady=10)

        form_frame = ttk.Frame(self.member_tab)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(form_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        self.member_email_entry = ttk.Entry(form_frame)
        self.member_email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Phone").grid(row=2, column=0, padx=5, pady=5)
        self.member_phone_entry = ttk.Entry(form_frame)
        self.member_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            self.member_tab,
            text="Add Member",
            command=self.add_member
        ).pack(pady=10)

        self.member_tree = ttk.Treeview(
            self.member_tab,
            columns=("ID", "Name", "Email", "Phone"),
            show="headings"
        )

        for col in ("ID", "Name", "Email", "Phone"):
            self.member_tree.heading(col, text=col)

        self.member_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_members()

    # =========================
    # Collection Tab
    # =========================

    def create_collection_tab(self):
        """Create collection/book management page."""
        ttk.Label(
            self.collection_tab,
            text="Add Library Collection",
            font=("Arial", 16)
        ).pack(pady=10)

        form_frame = ttk.Frame(self.collection_tab)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Title").grid(row=0, column=0, padx=5, pady=5)
        self.collection_title_entry = ttk.Entry(form_frame)
        self.collection_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Author").grid(row=1, column=0, padx=5, pady=5)
        self.collection_author_entry = ttk.Entry(form_frame)
        self.collection_author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Category").grid(row=2, column=0, padx=5, pady=5)
        self.collection_category_entry = ttk.Entry(form_frame)
        self.collection_category_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            self.collection_tab,
            text="Add Collection",
            command=self.add_collection
        ).pack(pady=10)

        self.collection_tree = ttk.Treeview(
            self.collection_tab,
            columns=("ID", "Title", "Author", "Category", "Status"),
            show="headings"
        )

        for col in ("ID", "Title", "Author", "Category", "Status"):
            self.collection_tree.heading(col, text=col)

        self.collection_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_collections()

    # =========================
    # Borrowing Tab
    # =========================

    def create_loan_tab(self):
        """Create borrowing transaction page."""
        ttk.Label(
            self.loan_tab,
            text="Create Borrowing Transaction",
            font=("Arial", 16)
        ).pack(pady=10)

        form_frame = ttk.Frame(self.loan_tab)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Member ID").grid(row=0, column=0, padx=5, pady=5)
        self.loan_member_id_entry = ttk.Entry(form_frame)
        self.loan_member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Collection ID").grid(row=1, column=0, padx=5, pady=5)
        self.loan_collection_id_entry = ttk.Entry(form_frame)
        self.loan_collection_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            self.loan_tab,
            text="Create Loan",
            command=self.create_loan
        ).pack(pady=10)

        ttk.Label(
            self.loan_tab,
            text="Note: Due date will automatically be 7 days after borrowing date."
        ).pack(pady=5)

    # =========================
    # Loan History Tab
    # =========================

    def create_history_tab(self):
        """Create loan history page."""
        ttk.Label(
            self.history_tab,
            text="Loan History",
            font=("Arial", 16)
        ).pack(pady=10)

        self.history_tree = ttk.Treeview(
            self.history_tab,
            columns=("Loan ID", "Member", "Collection", "Borrow Date", "Due Date"),
            show="headings"
        )

        for col in ("Loan ID", "Member", "Collection", "Borrow Date", "Due Date"):
            self.history_tree.heading(col, text=col)

        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(self.history_tab)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Refresh History",
            command=self.load_history
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Export PDF Report",
            command=self.export_loan_report
        ).grid(row=0, column=1, padx=5)

        self.load_history()

    # =========================
    # Load Data Methods
    # =========================

    def load_catalog(self):
        """Load all collections into catalog table."""
        self.catalog_tree.delete(*self.catalog_tree.get_children())

        for item in self.db.get_collections():
            self.catalog_tree.insert("", "end", values=item)

    def load_members(self):
        """Load members into member table."""
        self.member_tree.delete(*self.member_tree.get_children())

        for member in self.db.get_members():
            self.member_tree.insert("", "end", values=member)

    def load_collections(self):
        """Load collections into collection table."""
        self.collection_tree.delete(*self.collection_tree.get_children())

        for collection in self.db.get_collections():
            self.collection_tree.insert("", "end", values=collection)

    def load_history(self):
        """Load borrowing history into history table."""
        self.history_tree.delete(*self.history_tree.get_children())

        for loan in self.db.get_loans():
            self.history_tree.insert("", "end", values=loan)

    # =========================
    # Button Action Methods
    # =========================

    def add_member(self):
        """Add member from form input."""
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        phone = self.member_phone_entry.get()

        if not name or not email:
            messagebox.showerror("Error", "Name and email are required.")
            return

        self.db.add_member(name, email, phone)

        messagebox.showinfo("Success", "Member added successfully.")

        self.member_name_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)
        self.member_phone_entry.delete(0, tk.END)

        self.load_members()

    def add_collection(self):
        """Add collection from form input."""
        title = self.collection_title_entry.get()
        author = self.collection_author_entry.get()
        category = self.collection_category_entry.get()

        if not title or not author:
            messagebox.showerror("Error", "Title and author are required.")
            return

        self.db.add_collection(title, author, category)

        messagebox.showinfo("Success", "Collection added successfully.")

        self.collection_title_entry.delete(0, tk.END)
        self.collection_author_entry.delete(0, tk.END)
        self.collection_category_entry.delete(0, tk.END)

        self.load_collections()
        self.load_catalog()

    def create_loan(self):
        """Create borrowing transaction from form input."""
        member_id = self.loan_member_id_entry.get()
        collection_id = self.loan_collection_id_entry.get()

        if not member_id or not collection_id:
            messagebox.showerror("Error", "Member ID and Collection ID are required.")
            return

        try:
            self.db.create_loan(int(member_id), [int(collection_id)])
            messagebox.showinfo("Success", "Loan created successfully.")
        except ValueError:
            messagebox.showerror("Error", "Member ID and Collection ID must be numbers.")
            return
        except Exception as error:
            messagebox.showerror("Error", f"Failed to create loan: {error}")
            return

        self.loan_member_id_entry.delete(0, tk.END)
        self.loan_collection_id_entry.delete(0, tk.END)

        self.load_collections()
        self.load_catalog()
        self.load_history()

    def export_loan_report(self):
        """
        Export loan history to PDF using ReportLab external library.
        """
        loans = self.db.get_loans()

        try:
            filename = ReportGenerator.generate_loan_report(loans)
            messagebox.showinfo(
                "Success",
                f"PDF report generated successfully: {filename}"
            )
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Failed to generate PDF report: {error}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()