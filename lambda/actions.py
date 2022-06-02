import json
import boto3
from typing import Dict
# from aws_lambda_context import LambdaContext
# from botocore.exceptions import ClientError


def lambda_handler_0(event, context):

    method = event["httpMethod"]
    if method != 'GET':
        return {'statusCode': 403, 'body': 'Not Allowed'}
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    # if method == 'GET':
    #     lambda_1(event)
    # elif method == 'POST':
    #     lambda_2(event)


def lambda_handler_1(event, context):

    return {
        'statusCode': 200,
        'body': json.dumps(event)
        # 'body': json.dumps(event["pathParameters"])
        # 'body':
        #     event["queryStringParameters"]['key1'] +
        #     ". " +
        #     event["queryStringParameters"]['key2'] +
        #     ". " +
        #     event["queryStringParameters"]['key3'] +
        #     ". Hello CDK Watch!, changes"
    }


# def lambda_2(event: Dict):
#     s3 = boto3.resource('s3')
#     # bucket_name = event["queryStringParameters"]['bucket']
#     bucket_name = 'restevean-first-bucket'
#     object_name = event["queryStringParameters"]['object']
#     bucket = s3.Bucket(bucket_name)
#     objs = list(bucket.objects.filter(Prefix=object_name))
#
#     if len(objs) <= 0:
#         bucket.put_object(Bucket=bucket_name, Key=object_name)
#         return {
#             'statusCode': 201,
#             'body': json.dumps(f'Created object {object_name} on {bucket_name}')
#             # 'body': json.dumps(event)
#         }
#     else:
#         return {
#             'statusCode': 409,
#             'body': json.dumps(f'object {object_name} already exists on {bucket_name}')
#             # 'body': json.dumps(event)
#         }
