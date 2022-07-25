from typing import Any
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_iam as iam,
    aws_cognito as cognito, RemovalPolicy,
)
from constructs import Construct


# TODO: Actually any user from user_pool is allowed to create users, only users from admin_users might be able
# TODO: Testing
# TODO: Custom domain in stack, Route53
# TODO: user_to_group.add_depends_on(target(CfnResource))


class SidikeyStack(Stack):

    def __init__(self, scope: Construct, id_: str, **kwargs: Any) -> None:
        super().__init__(scope, id_, **kwargs)

        lambda_layer = _lambda.LayerVersion(
            self, 'lambda-layer',
            # code=_lambda.AssetCode('lambda/layer/'),
            code=_lambda.AssetCode('.lambda_layers_dependencies/'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        )

        # Defines an AWS Lambda resource, my_lambda_0
        my_lambda_0 = _lambda.Function(
            self, 'handler_0',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='api_root, root of Sidikey API gateway',
            handler='actions.api_root',
            layers=[lambda_layer],
            function_name='handler_root'
        )

        # Defines an AWS Lambda resource, my_lambda_1
        my_lambda_1 = _lambda.Function(
            self, 'handler_1',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 1, method "GET" on resource /testing',
            handler='actions.lambda_handler_1',
            layers=[lambda_layer],
            function_name='testing_get'
        )

        # Defines an AWS Lambda resource, my_lambda_2
        my_lambda_2 = _lambda.Function(
            self, 'handler_2',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 2, method "POST" on resource /testing',
            handler='actions.lambda_handler_2',
            layers=[lambda_layer],
            function_name='testing_post'
        )

        # Defines an AWS Lambda resource, my_lambda_3
        my_lambda_3 = _lambda.Function(
            self, 'handler_3',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 3, method "PUT" on resource /testing',
            handler='actions.lambda_handler_3',
            layers=[lambda_layer],
            function_name='testing_put'
        )

        my_lambda_4 = _lambda.Function(
            self, 'handler_4',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            description='Handler 4, method "POST" on resource /useradd',
            handler='actions.add_user_to_pool',
            layers=[lambda_layer],
            function_name='adding_users'
        )

        # Defines cognito user pool
        # core.CfnResource(self, "UserPoolCfnResource", type="AWS::COGNITO::USERPOOL")
        user_pool = cognito.UserPool(self, 'MyUserPool05',
                                     user_pool_name='Sidikey_User_Pool',
                                     standard_attributes=cognito.StandardAttributes(
                                         email=cognito.StandardAttribute(
                                             required=True,
                                             mutable=True
                                         )
                                     ),
                                     self_sign_up_enabled=False,
                                     auto_verify=cognito.AutoVerifiedAttrs(email=True, phone=False),
                                     account_recovery=cognito.AccountRecovery.EMAIL_ONLY,

                                     # removal_policy=RemovalPolicy.DESTROY,
                                     )

        # Assign an app client to created cognito pool
        user_pool_cli = user_pool.add_client("SidikeyApp01",
                                             o_auth=cognito.OAuthSettings(
                                                 flows=cognito.OAuthFlows(
                                                     authorization_code_grant=True,
                                                     implicit_code_grant=True,
                                                 ),
                                                 scopes=[cognito.OAuthScope.EMAIL],
                                                 callback_urls=["https://api.restevean.es"],
                                                 logout_urls=["https://api.restevean.es"]
                                             ),
                                             )

        # Assign a domain to the user pool
        user_pool_domain = user_pool.add_domain("resteveandomain13",
                                                cognito_domain=cognito.CognitoDomainOptions(
                                                    domain_prefix="sidikeydomain"
                                                ),
                                                )

        # Defines an AWS API Gateway resource and assign as a trigger for my_lambda_0
        api = apigw.LambdaRestApi(
            self, 'Sidikey',
            handler=my_lambda_0,
            proxy=False,
            # default_domain_mapping={"api.restevean.es": dn},
        )

        # Create a user Admin and attach it to the cognito_user_admin_group
        cognito.CfnUserPoolUser(self, "Admin",
                                user_pool_id=user_pool.user_pool_id,
                                username="Admin",
                                # desired_delivery_mediums=["desiredDeliveryMediums"],
                                # message_action="RESEND",
                                user_attributes=[
                                    cognito.CfnUserPoolUser.AttributeTypeProperty(
                                        name="email",
                                        value="resteve24@gmail.com"
                                    ),
                                    cognito.CfnUserPoolUser.AttributeTypeProperty(
                                        name="email_verified",
                                        value="True"
                                    )],
                                )

        # Create a role
        cognito_admin_user_role = iam.Role(self, "Role",
                                           assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                                           description="Can add user to the pool"
                                           )

        # Create a cognito user group
        cognito.CfnUserPoolGroup(self, "my_admin_users",
                                 user_pool_id=user_pool.user_pool_id,
                                 description="Users that can add users to the cognito pool",
                                 group_name="admin_users",
                                 precedence=1,
                                 role_arn=cognito_admin_user_role.role_arn
                                 )

        # Set up role permissions
        add_user_policy = iam.PolicyStatement(
            actions=[
                "cognito-idp:AdminEnableUser",
                "cognito-idp:AdminCreateUser",
                "cognito-idp:AdminDisableUser",
            ],
            resources=[user_pool.user_pool_arn]
        )
        cognito_admin_user_role.add_to_policy(add_user_policy)
        my_lambda_4.add_to_role_policy(add_user_policy)

        # cognito_admin_user_role.add_to_policy(iam.PolicyStatement(
        #     actions=[
        #         "cognito-idp:AdminEnableUser",
        #         "cognito-idp:AdminCreateUser",
        #         "cognito-idp:AdminDisableUser"
        #     ],
        #     resources=[user_pool.user_pool_arn]
        # ),
        # )
        #
        # my_lambda_4.add_to_role_policy(iam.PolicyStatement(
        #     actions=[
        #         "cognito-idp:AdminEnableUser",
        #         "cognito-idp:AdminCreateUser",
        #         "cognito-idp:AdminDisableUser"
        #     ],
        #     resources=[user_pool.user_pool_arn]
        # ),
        # )

        # Creates an authorizer
        my_authorizer = apigw.CognitoUserPoolsAuthorizer(self, "SidikeyAuthorizer",
                                                         cognito_user_pools=[user_pool],
                                                         )

        # Creating API resources and methods
        # api.root.add_method("GET", )
        api.root.add_method("GET",
                            # authorizer=authorizer,
                            authorizer=my_authorizer,
                            authorization_type=apigw.AuthorizationType.COGNITO,
                            )
        api.root.add_method("POST")
        new_resource = api.root.add_resource("testing")
        get_method_integration = apigw.LambdaIntegration(my_lambda_1)
        post_method_integration = apigw.LambdaIntegration(my_lambda_2)
        put_method_integration = apigw.LambdaIntegration(my_lambda_3)
        new_resource.add_method("GET", get_method_integration)  # GET /testing
        new_resource.add_method("POST", post_method_integration)  # POST /testing
        new_resource.add_method("PUT", put_method_integration)  # PUT /testing
        nr_user_add = api.root.add_resource("useradd")
        post_method_integration = apigw.LambdaIntegration(my_lambda_4)
        nr_user_add.add_method("POST", post_method_integration,
                               authorizer=my_authorizer,
                               authorization_type=apigw.AuthorizationType.COGNITO,
                               )  # POST /useradd

        # Defines an AWS s3 bucket to create (if does not exist)
        s3.Bucket(
            self,
            'restevean-cdk-bucket',
            bucket_name='restevean-cdk-bucket',
            removal_policy=RemovalPolicy.DESTROY
        )

        # Gives read/write permission from my_lambda_2 to the bucket
        # 👇 I think line below is not good practice, but it works.
        # 👇 To make it work uncomment line 89 and comment line 90
        # bucket.grant_read_write(my_lambda_2)

        # Defines and add permissions to my_lambda_2
        my_lambda_2.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:ListBucket", "s3:PutObject"],
            effect=iam.Effect.ALLOW,
            resources=['arn:aws:s3:::restevean-cdk-bucket', 'arn:aws:s3:::restevean-cdk-bucket/*']
        )
        )

        """
        # I think this is the most precise way, but means more lines of code than ☝️ previoous way ☝
        my_lambda_2.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:ListBucket"],
            effect=iam.Effect.ALLOW,
            resources=['arn:aws:s3:::restevean-cdk-bucket']
            )
        )
        my_lambda_2.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:PutObject"],
            effect=iam.Effect.ALLOW,
            resources=['arn:aws:s3:::restevean-cdk-bucket/*']
            )
        )
        """
        cognito.CfnUserPoolUserToGroupAttachment(self, "MyCfnUserPoolUserToGroupAttachment",
                                                 group_name="admin_users",
                                                 username="Admin",
                                                 user_pool_id=user_pool.user_pool_id,
                                                 )
        # user_to_group.add_depends_on(target(CfnResource))
