from decouple import config
import boto3

sqs = boto3.client(
    'sqs',
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    region_name=config("AWS_REGION"),
    )

sqs_url = config("SQS_URL")