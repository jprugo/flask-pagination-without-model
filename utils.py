import boto3
from re import sub, MULTILINE
from json import loads
from botocore.exceptions import ClientError

def get_s3_client():
    return boto3.client('s3')

def get_scm_client():
    return boto3.client('secretsmanager', region_name='us-east-1')

def get_script_content(bucket: str, key_path: str):
    """
        Retrieves the script stored in an s3 bucket (AWS)
        :param bucket: Bucket name from which the script will be retrieved
        :type bucket: string
        :type key_path: string
        :param key_path: file name with extension
            You must first make sure that you have the permissions on the resource to invoke
                :py:meth:`key_path.sql`.
        :raises
                BucketReadFileException: If bucket is None ad file is None or query is None.
                Exception: normal exception
        :return: Script file content
    """
    try:
        bucket = sub(r".*:(.*?)", '', bucket, 0, MULTILINE)
        data = get_s3_client().get_object(Bucket=bucket, Key=key_path)
        return data['Body'].read().decode('utf-8')
    except ClientError as e:
        raise e
    except Exception as e:
        raise e

def get_connection_data(secret_id: str) -> dict:
    
    """
    Retrieves the secret value stored through secrets Manager (AWS) with the connection to the different database
    sources.
        :type secret_id: string
        :param secret_id: Arn from the Secrets Manager resource
            You must first make sure that you have the permissions on the resource to invoke
        :raises
                SecretManagerException: If bucket is None ad file is None or query is None.
                Exception: normal exception
        :return: Secrets manager data dumped
    """
    try:
        data = get_scm_client().get_secret_value(
            SecretId=secret_id
        )
        if isinstance(data, str):
            data = loads(data)
        return data['SecretString']
    except ClientError as e:
        raise e
    except Exception as e:
        raise e
