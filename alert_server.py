import smtplib
from email.message import EmailMessage
from typing import List
import imghdr
import os

class AlertServer:
    def __init__(self):
        # Define Source Email Address
        self.user = 'alert_email'
        self.password = 'password'

    def create_message(self, subject: str, body: str, to: str, images: List[str] = []) -> EmailMessage:
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['from'] = self.user
        msg['to'] = to

        for img in images:
            file = open(img, 'rb')
            img_data = file.read()
            image_type = imghdr.what(file.name)
            image_name = os.path.basename(file.name)
            msg.add_attachment(img_data, maintype='image', subtype=image_type, filename=image_name)

        return msg

    def send_message(self, msg: EmailMessage):
        # Connect to server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.user, self.password)

        # Send message
        server.send_message(msg)

        # Disconnect from server
        server.quit()

    def send_email(self, subject: str, body: str, images: List[str] = []):
        msg = self.create_message(subject, body, 'recipient_email@gmail.com', images)
        self.send_message(msg)

    def send_text(self, subject: str, body: str):
        msg = self.create_message(subject, body, '1238675309@msg.fi.google.com')
        self.send_message(msg)

    def send_all(self, subject: str, body: str):
        self.send_email(subject, body)
        self.send_text(subject, body)
    
# Test function
if __name__ == '__main__':
    alert = AlertServer()
    alert.send_all('Test', 'This is a test')