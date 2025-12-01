#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3', region_name='us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')

#Create an S3 Bucket
def create_s3_bucket(bucket_name, region='us-east-1'):
    """Create an S3 bucket"""
    try:
        if region == 'us-east-1':
            
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"✓ Bucket '{bucket_name}' created successfully")
        return True
    except ClientError as e:
        print(f"✗ Error: {e}")
        return False


#Create a DynamoDB Table
def create_dynamodb_table(table_name):
    """Create a DynamoDB table"""
    try:
        response = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'LockID', 'KeyType': 'HASH'},  # Partition key (era 'STRING', debe ser 'HASH')
            ],  # Faltaba esta coma
            AttributeDefinitions=[  # Faltaba esta sección completa
                {'AttributeName': 'LockID', 'AttributeType': 'S'}  # 'S' = String
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand billing
        )
        print(f"✓ Table '{table_name}' created successfully")
        return response
    except ClientError as e:
        print(f"✗ Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Create S3 bucket
    create_s3_bucket('my-terraform-state-bucket-nikovi')
    
    # Create DynamoDB table
    create_dynamodb_table('terraform-state-lock-nikovi')