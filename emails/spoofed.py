# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from utils.config import SMTP


class SendSpoofed:
    def __init__(self, sender_email, receiver_email, subject, html_content):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.html_content = html_content

    def send_email(self):
        message = MIMEMultipart()
        message.attach(MIMEText(self.html_content, "html"))
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        smtp_server = SMTP.get("server", "smtp.mailersend.net")
        smtp_port = int(SMTP.get("port", 587))
        smtp_username = SMTP.get("username", "")
        smtp_password = SMTP.get("password", "")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            print("Email sent successfully!")
