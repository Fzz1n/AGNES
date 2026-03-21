import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = os.environ["smtp_server"]
PORT = os.environ["smtp_port"]
SENDER_EMAIL = os.environ["sender_email"]
PASSWORD = os.environ["sender_email_password"]
RECIVER_EMAIL = os.environ["receiver_email"]

def send_email(title, body = "", file_path = None):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECIVER_EMAIL
    message["Subject"] = title

    # Creation of mail body
    body += "<br><b>Best regards AGNES</b>"
    message.attach(MIMEText(body, 'html'))

    # Attach file
    if file_path is not None:
        message = attach_txt_file(message, file_path)
        if isinstance(message, str):
            return message

    # Send the mail
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(message)
        print("email send")
    except smtplib.SMTPAuthenticationError:
        print('Authentication failed. Check your username and password.')
    except smtplib.SMTPConnectError:
        print('Failed to connect to the SMTP server.')
    except smtplib.SMTPRecipientsRefused:
        print('One or more recipients were rejected.')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        server.quit()

# attach a txt file to the email
def attach_txt_file(message, file_path):
    # Get teh file name from the path
    file_arr = file_path.split("/")
    filename = file_arr[len(file_arr)-1]
    try:
        with open(file_path) as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)

            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            message.attach(part)
    except:
        return "File not found"
    return message