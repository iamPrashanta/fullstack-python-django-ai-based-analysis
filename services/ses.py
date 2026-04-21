
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SESService:
    def __init__(self):
        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_SES_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SES_SECRET_ACCESS_KEY,
            region_name=settings.AWS_SES_REGION_NAME
        )
        self.sender_email = settings.DEFAULT_FROM_EMAIL

    def send_email(self, recipient_email, subject, body_text, body_html=None):
        """Send an email using SES."""
        charset = "UTF-8"
        
        destination = {
            'ToAddresses': [recipient_email],
        }
        
        message = {
            'Subject': {
                'Data': subject,
                'Charset': charset
            },
            'Body': {
                'Text': {
                    'Data': body_text,
                    'Charset': charset
                }
            }
        }
        
        if body_html:
            message['Body']['Html'] = {
                'Data': body_html,
                'Charset': charset
            }

        try:
            response = self.ses_client.send_email(
                Destination=destination,
                Message=message,
                Source=self.sender_email,
            )
        except ClientError as e:
            logger.error(f"Failed to send email via SES: {e}")
            raise
        else:
            logger.info(f"Email sent! Message ID: {response['MessageId']}")
            return response['MessageId']
