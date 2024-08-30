import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from twilio.rest import Client
from src.rag_agent.notifications.config import NOTIFICATION_CHANNELS, NOTIFICATION_TYPES
from src.rag_agent.utils.logging_config import logger

class NotificationService:
    def __init__(self):
        self.channels = NOTIFICATION_CHANNELS

    def send_notification(self, notification_type, message):
        channels = NOTIFICATION_TYPES.get(notification_type, [])
        for channel in channels:
            if self.channels[channel]['enabled']:
                method_name = f'_send_{channel}_notification'
                if hasattr(self, method_name):
                    getattr(self, method_name)(message)
                else:
                    logger.warning(f"Notification method not implemented for channel: {channel}")

    def _send_email_notification(self, message):
        try:
            email_config = self.channels['email']
            msg = MIMEMultipart()
            msg['From'] = email_config['smtp_username']
            msg['To'] = ', '.join(email_config['recipients'])
            msg['Subject'] = "RAG Agent Notification"
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['smtp_username'], email_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            logger.info("Email notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")

    def _send_slack_notification(self, message):
        try:
            slack_config = self.channels['slack']
            payload = {'text': message}
            response = requests.post(slack_config['webhook_url'], json=payload)
            if response.status_code == 200:
                logger.info("Slack notification sent successfully")
            else:
                logger.error(f"Failed to send Slack notification. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")

    def _send_sms_notification(self, message):
        try:
            sms_config = self.channels['sms']
            client = Client(sms_config['twilio_account_sid'], sms_config['twilio_auth_token'])
            message = client.messages.create(
                body=message,
                from_=sms_config['twilio_phone_number'],
                to=sms_config['recipient_phone_number']
            )
            logger.info(f"SMS notification sent successfully. SID: {message.sid}")
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")

notification_service = NotificationService()
