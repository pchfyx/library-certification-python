from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


class ReportGenerator:
    """
    ReportGenerator class uses the external ReportLab library
    to generate a PDF report for loan history.
    """

    @staticmethod
    def generate_loan_report(loans, filename="loan_report.pdf"):
        """
        Generate a PDF report from loan history data.

        Parameters:
            loans: list of loan history records
            filename: output PDF file name
        """
        pdf = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        pdf.setTitle("Library Loan Report")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 50, "Library Loan Report")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 70, f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        y = height - 110

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, "Loan ID")
        pdf.drawString(110, y, "Member")
        pdf.drawString(240, y, "Collection")
        pdf.drawString(390, y, "Borrow Date")
        pdf.drawString(480, y, "Due Date")

        y -= 20
        pdf.setFont("Helvetica", 9)

        if not loans:
            pdf.drawString(50, y, "No loan data available.")
        else:
            for loan in loans:
                if y < 50:
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont("Helvetica", 9)

                loan_id, member_name, collection_title, borrow_date, due_date = loan

                pdf.drawString(50, y, str(loan_id))
                pdf.drawString(110, y, str(member_name)[:22])
                pdf.drawString(240, y, str(collection_title)[:25])
                pdf.drawString(390, y, str(borrow_date))
                pdf.drawString(480, y, str(due_date))

                y -= 18

        pdf.save()
        return filename