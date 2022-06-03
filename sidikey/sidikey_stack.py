from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
)
# TODO: s3, layers, poetry

class SidikeyStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda_0 = _lambda.Function(
            self, 'Handler_0',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='actions.lambda_handler_0',
        )

        # Defines an AWS Lambda resource
        my_lambda_1= _lambda.Function(
            self, 'Handler_1',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='actions.lambda_handler_1',
        )

        # Defines an AWS Lambda resource
        my_lambda_2= _lambda.Function(
            self, 'Handler_2',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='actions.lambda_handler_2',
        )

        # Defines an AWS API Gateway resource and assign as a trigger for my_lambda
        api = apigw.LambdaRestApi(
            self, 'Sidikey',
            handler=my_lambda_0,
            proxy=False,
        )
        api.root.add_method("GET")
        api.root.add_method("POST")
        items = api.root.add_resource("testing")
        get_method_integration = apigw.LambdaIntegration(my_lambda_1)
        post_method_integration = apigw.LambdaIntegration(my_lambda_2)
        items.add_method("GET", get_method_integration)  # GET /items
        items.add_method("POST", post_method_integration)  # POST /items

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
