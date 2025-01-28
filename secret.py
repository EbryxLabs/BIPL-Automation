import boto3
from botocore.exceptions import ClientError
import json

def get_secret():

    secret_name = "mss/site/mssp"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        print("Error getting secret", e)
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    data = json.loads(secret)
    client_secret = data['client_secret']
    print("Secret extracted", client_secret)
    return client_secret
#get_secret()
