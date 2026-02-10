import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()
app_password = os.getenv("APP_PASSWORD")
sender = os.getenv("SENDER_EMAIL")

def send_email(receiver_email: str, subject: str, content: str):
    """
    Send an email to the specified receiver.

    Args:
        receiver_email: The email address of the person receiving the email.
        subject: The subject line of the email.
        content: The main body text of the email.
    """
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver_email

    # Connect to Gmail SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.send_message(msg)
    print("Email sent successfully!")

if __name__ == "__main__":
    send_email(receiver_email="4mh23cs158@gmail.com", subject="Hello", content="This is a test email")
