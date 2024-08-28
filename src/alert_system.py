import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AlertSystem:
    def __init__(self, recipient_email):
        self.recipient_email = recipient_email
        self.sender_email = "shauryamsingh9@gmail.com"
        self.password = "Legitkillerop&540"  # Use app password here

    def send_alert(self, message):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = 'Alert Notification'

        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
                print("Alert sent successfully!")
        except Exception as e:
            print(f"Failed to send alert: {e}")
