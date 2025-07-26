import os
from twilio.rest import Client
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
TARGET_PHONE = os.getenv("TARGET_PHONE")
EMAIL = os.getenv("EMAIL")
EMAIL_PWD = os.getenv("EMAIL_PWD")

class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH)

    def send_sms(self, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_=TWILIO_PHONE,
                to=TARGET_PHONE
            )
            print("SMS sent:", message.sid)
        except Exception as e:
            print("SMS failed:", e)

    from email.message import EmailMessage

    def send_email(self, subject, body, to_email):
        try:
            msg = EmailMessage()
            msg["From"] = EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(body)

            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=EMAIL_PWD)
                connection.send_message(msg)

            print("Email sent")
        except Exception as e:
            print("Email failed:", e)

