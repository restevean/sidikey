import json
import boto3
# from typing import Dict


def api_root(event, context):
    method: str = event["httpMethod"]
    if method == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    else:
        return {'statusCode': 403, 'body': 'Not Allowed'}


def lambda_handler_1(event, context):
    return {'statusCode': 200, 'body': 'Handler 1, method "GET"'}


def lambda_handler_2(event, context):
    s3 = boto3.resource('s3')
    bucket_name = event["queryStringParameters"]['bucket']
    object_name = event["queryStringParameters"]['object']
    bucket = s3.Bucket(bucket_name)
    objs = list(bucket.objects.filter(Prefix=object_name))

    if len(objs) <= 0:
        bucket.put_object(Bucket=bucket_name, Key=object_name)
        return {
            'statusCode': 201,
            'body': json.dumps(f'Created object {object_name} on {bucket_name}')
            # 'body': json.dumps(event)
        }
    else:
        return {
            'statusCode': 409,
            'body': json.dumps(f'object {object_name} already exists on {bucket_name}')
            # 'body': json.dumps(event)
        }


def lambda_handler_3(event, context):
    return {'statusCode': 200, 'body': 'Handler 3, method "PUT"'}
