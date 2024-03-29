from decouple import config
import boto3

sns = boto3.client(
    'sns',
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    region_name=config("AWS_REGION"),
    )

sns_arn = config("SNS_ARN")