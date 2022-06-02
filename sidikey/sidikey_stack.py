from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
)


class SidikeyStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda1 = _lambda.Function(
            self, 'Handler_1',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='actions.lambda_handler_0',
        )

        # Defines an AWS API Gateway resource and assign as a trigger for my_lambda
        api = apigw.LambdaRestApi(
            self, 'Sidikey',
            handler=my_lambda1,
            proxy=False,
        )
        # api.root.add_method("GET")
        items = api.root.add_resource("testing")
        items.add_method("GET")  # GET /items
        items.add_method("POST")  # POST /items


# class S3DeployStack(Stack):
#
#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)
#
#         s3.Bucket(
#             self,
#             'restevean-cdk-bucket',
#             bucket_name = 'restevean-cdk-bucket'
#         )
