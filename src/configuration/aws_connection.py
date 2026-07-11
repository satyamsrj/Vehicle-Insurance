import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

from src.constants import (
    AWS_ACCESS_KEY_ID_ENV_KEY,
    AWS_SECRET_ACCESS_KEY_ENV_KEY,
    REGION_NAME,
)

# Project root (Vehicle-Insurance/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env from project root
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)


class S3Client:

    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        """
        This class gets AWS credentials from the .env file/environment
        and creates a connection with the S3 bucket.
        """

        if S3Client.s3_client is None or S3Client.s3_resource is None:

            access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

            if not access_key_id:
                raise Exception(
                    f"Environment variable '{AWS_ACCESS_KEY_ID_ENV_KEY}' is not set. "
                    f"Expected .env at: {BASE_DIR / '.env'}"
                )

            if not secret_access_key:
                raise Exception(
                    f"Environment variable '{AWS_SECRET_ACCESS_KEY_ENV_KEY}' is not set. "
                    f"Expected .env at: {BASE_DIR / '.env'}"
                )

            S3Client.s3_resource = boto3.resource(
                service_name="s3",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name,
            )

            S3Client.s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name,
            )

        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client