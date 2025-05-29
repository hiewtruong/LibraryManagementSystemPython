import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from domain.dto.transaction.transaction_send_email_dto import TransactionSendEmailDTO
from domain.dto.book.book_send_email_dto import BookSendEmail
from datetime import datetime

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = "hieutg02198@gmail.com"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("hieutg02198@gmail.com", "nekmikwwmnfkzubas")
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
@staticmethod
def generate_account_email_content(user_name: str, password: str) -> str:
        return f"""
        <html><body>
            <h3>Hello {user_name},</h3>
            <p>Your account has been successfully created. Below are your login details:</p>
            <ul>
                <li><strong>Username:</strong> {user_name}</li>
                <li><strong>Password:</strong> {password}</li>
            </ul>
            <p>Wish you have a good time using the system for booking books.</p>
            <br>
            <hr>
            <p style='font-size: 12px; color: gray;'>This is an automated message. Please do not reply to this email.</p>
        </body></html>
        """

@staticmethod
def generate_loan_email_content(transaction: TransactionSendEmailDTO) -> str:
        loan_dt = transaction.loan_dt.strftime("%m/%d/%Y") if isinstance(transaction.loan_dt, datetime) else str(transaction.loan_dt)
        return_dt = transaction.loan_return_dt.strftime("%m/%d/%Y") if isinstance(transaction.loan_return_dt, datetime) else str(transaction.loan_return_dt)

        content = f"""
        <html><body>
            <h3>Hello {transaction.use_name},</h3>
            <p>Your book loan request has been successfully recorded. Below are the loan details:</p>
            <ul>
                <li><strong>Loan Ticket Number:</strong> {transaction.loan_ticket_number}</li>
                <li><strong>Email:</strong> {transaction.email}</li>
                <li><strong>Phone:</strong> {transaction.phone}</li>
                <li><strong>Total Quantity:</strong> {transaction.total_qty}</li>
                <li><strong>Loan Date:</strong> {loan_dt}</li>
                <li><strong>Return Date:</strong> {return_dt}</li>
            </ul>
            <h4>Book Details</h4>
            <table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse;'>
                <tr style='background-color: #f2f2f2;'>
                    <th>ID</th><th>Title</th><th>Author</th>
                </tr>
        """

        for book in transaction.book_details:
            content += f"""
                <tr>
                    <td>{book.book_id}</td>
                    <td>{book.title}</td>
                    <td>{book.author}</td>
                </tr>
            """

        content += """
            </table>
            <br><hr>
            <p style='font-size: 12px; color: gray;'>This is an automated message. Please do not reply to this email.</p>
        </body></html>
        """
        return content