import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = os.environ["smtp_server"]
PORT = os.environ["smtp_port"]
SENDER_EMAIL = os.environ["sender_email"]
PASSWORD = os.environ["sender_email_password"]
RECIVER_EMAIL = os.environ["receiver_email"]

def send_email(title, body):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECIVER_EMAIL
    message["Subject"] = title

    # Creation of mail body
    message.attach(MIMEText(body, 'plain'))

    # Send the mail
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(message)
        server.quit()
    except:
        return "An error accure when trying to send a email"
    else:
        return "Email send"