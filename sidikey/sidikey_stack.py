from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
)


# TODO: s3 use an existing bucket, permissions, layers, , testing, poetry


class SidikeyStack(Stack):

    def __init__(self, scope: Construct, id_: str, **kwargs) -> None:
        super().__init__(scope, id_, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda_0 = _lambda.Function(
            self, 'Handler_0',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 0, root of Sidikey API gateway',
            handler='actions.lambda_handler_0',
        )

        # Defines an AWS Lambda resource
        my_lambda_1 = _lambda.Function(
            self, 'Handler_1',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 1, method "GET" on resource /testing',
            handler='actions.lambda_handler_1',
        )

        # Defines an AWS Lambda resource
        my_lambda_2 = _lambda.Function(
            self, 'Handler_2',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 1, method "POST" on resource /testing',
            handler='actions.lambda_handler_2',
        )

        # Defines an AWS Lambda resource
        my_lambda_3 = _lambda.Function(
            self, 'Handler_3',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 1, method "PUT" on resource /testing',
            handler='actions.lambda_handler_3',
        )

        # Defines an AWS API Gateway resource and assign as a trigger for my_lambda_0
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
        put_method_integration = apigw.LambdaIntegration(my_lambda_3)
        items.add_method("GET", get_method_integration)  # GET /items
        items.add_method("POST", post_method_integration)  # POST /items
        items.add_method("PUT", put_method_integration)  # PUT /items

        # Defines an AWS s3 bucket to create (does not exist until deployment)
        s3.Bucket(
            self,
            'restevean-cdk-bucket',
            bucket_name='restevean-cdk-bucket'
        )
