import os
from dotenv import load_dotenv

load_dotenv(override=False)


class Config:
    APP_NAME = os.environ['APP_NAME']

    # Environment
    ENVIRONMENT = os.environ['ENVIRONMENT']
    REGION = os.environ['REGION']

    # Log
    LOG_LEVEL = os.environ['LOG_LEVEL']
    LOG_FILE_INFO = os.environ['LOG_FILE_INFO']
    LOG_FILE_ERROR = os.environ['LOG_FILE_ERROR']

    # Mongodb
    MONGODB = {
        'user': os.environ.get('MONGODB_USER'),
        'password': os.environ.get('MONGODB_PASSWORD'),
        'host': os.environ.get('MONGODB_HOST'),
        'port': os.environ.get('MONGODB_PORT'),
        'database': os.environ.get('MONGODB_DATABASE'),
    }

    # AWS
    AWS = {
        's3_key_id': os.getenv('AWS_S3_KEY_ID'),
        's3_key_secret': os.getenv('AWS_S3_SECRET_KEY'),
        'region': os.getenv('AWS_S3_REGION'),
        'dynamo_table': os.getenv('AWS_DYNAMO_TABLE')
    }
