import json
import boto3
import base64
from botocore.exceptions import ClientError
 
def lambda_handler(event, context):
    # Specify the name of your secret in AWS Secrets Manager
    environment = event['env']
    secret_name = "adinath/%s/key" % environment
    region_name = "us-east-1"
 
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        # Get the secret value
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as error:
        print(error)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(error)})
        }
    if 'SecretString' in secret_value_response:
        secret = json.loads(secret_value_response['SecretString'])
        return secret
    else:
        try:
            decoded_binary_secret = base64.b64decode(secret_value_response['SecretBinary'])
            return decoded_binary_secret
        except Exception as binary_decode_error:
            print(binary_decode_error)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(binary_decode_error)})
            }
