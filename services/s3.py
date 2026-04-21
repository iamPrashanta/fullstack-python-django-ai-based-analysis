
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_obj, object_name):
        """Upload a file-like object to S3."""
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name)
            return f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{object_name}"
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

    def generate_presigned_url(self, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object"""
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': self.bucket_name,
                                                                     'Key': object_name},
                                                             ExpiresIn=expiration)
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None
        return response
