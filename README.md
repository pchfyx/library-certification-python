# Library Certification App

The Library Certification App is a simple desktop application designed to manage library catalogs and record collection loans by library members.

This application was built to fulfill the practical demonstration assignment for the Programmer certification.

## Application Features

1. Display the library collection catalog.
2. Add library member data.
3. Add library collection or book data.
4. Record borrowing/loan transactions.
5. Automatically calculate the return due date (7 days after the borrowing date).
6. Display borrowing history.
7. Export borrowing reports to PDF.
8. Perform unit testing on the core features of the application.

## Technologies Used

- Python
- Tkinter
- SQLite
- ReportLab
- unittest

## Database Structure

This application uses an SQLite database with several main tables:

### 1. members

Used to store library member data.


| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Member name |
| email | TEXT | Member email |
| phone | TEXT | Member phone number |

### 2. collections

Used to store library collection or book data.


| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Collection title |
| author | TEXT | Author |
| category | TEXT | Category |
| status | TEXT | Collection status (Available or Borrowed) |

### 3. loans

Used to store loan transaction data.


| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| member_id | INTEGER | Foreign key referencing the members table |
| borrow_date | TEXT | Borrowing date |
| due_date | TEXT | Return due date |

### 4. loan_items

Used to store specific details of the collections borrowed within a loan transaction.


| Field | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| loan_id | INTEGER | Foreign key referencing the loans table |
| collection_id | INTEGER | Foreign key referencing the collections table |

## External Library

This application uses the following external library:

```text
ReportLab
```
*ReportLab is utilized to generate loan history reports as PDF files.*

## How to Run the Application

1. **Clone this repository:**
   ```bash
   git clone URL_REPOSITORY
   ```
2. **Navigate into the project folder:**
   ```bash
   cd library-certification-python
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```

## How to Run Unit Testing

Execute the following command in your terminal:

```bash
python -m unittest test_loan_service.py
```

If all tests pass successfully, the output will display:

```text
OK
```

## Program Modules

* **`app.py`**  
  The main file to launch the desktop application using Tkinter. This file handles the user interface, layout, and tabs for the catalog, members, collections, borrowing, and loan history.

* **`database.py`**  
  The file responsible for managing the SQLite database connection, creating tables, adding member records, adding collections, logging borrowing transactions, and fetching history details.

* **`report_generator.py`**  
  The file designed to generate structured PDF reports utilizing the external ReportLab library.

* **`test_loan_service.py`**  
  The file designated for executing unit tests on the application's core functionality, including adding members, adding collections, processing loans, validating due dates, and tracking collection status switches.

## Test Scenarios


| No | Scenario | Expected Result |
|---|---|---|
| 1 | Add a member | Member data is successfully saved. |
| 2 | Add a collection | Collection data is successfully saved. |
| 3 | Create a loan | Loan transaction data is successfully saved. |
| 4 | Check the due date | Due date is automatically set to exactly 7 days after the borrowing date. |
| 5 | Check collection status | Collection status changes to `Borrowed` immediately after it is loaned out. |

## Conclusion

This application serves as a simple library system capable of displaying a catalog, logging member profiles, tracking inventory assets, processing loan flows, auto-calculating due windows, generating PDF summary outputs, and running structural unit tests.
