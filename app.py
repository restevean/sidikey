# !/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_stacks.sidikey_stack import SidikeyStack
import subprocess
# from cdk_stacks.sidikey_stack import S3DeployStack
# from dotenv import load_dotenv
# import MODULE_NAME as MODULE_NAME


# ENVIRONMENT_TYPE = os.environ.get("ENVIRONMENT_TYPE", "sandbox")
# PROJECT_NAME = "sidikey"
# MODULE_NAME = "your-module-name"  # Remove this if this is a non-portal project

# if ENVIRONMENT_TYPE not in ['sandbox', 'dev', 'test', 'prod']:
#     raise Exception(
#         'Invalid value for the ENVIRONMENT_TYPE environment variable. Must be '
#         'one of [sandbox, dev, test, prod].'
#     )
#
# LAMBDA_LOG_LEVEL_PER_ENVIRONMENT = {
#     'sandbox': 'DEBUG',
#     'dev': 'DEBUG',
#     'test': 'WARNING',
#     'prod': 'WARNING'
# }

if not os.path.exists('.lambda_layers_dependencies'):
    os.makedirs('.lambda_layers_dependencies')

subprocess.check_output(
    [
        'poetry',
        'export',
        '-f',
        'requirements.txt',
        '--without-hashes',
        '--with-credentials',
        '--output',
        '.lambda_layers_dependencies/requirements.txt'
    ]
)


app = cdk.App()
SidikeyStack(app,
             "SidikeyStack",
             # stack_name='sidikey-stack',
             # environment_type=ENVIRONMENT_TYPE,
             # project_name=PROJECT_NAME,
             # module_name=MODULE_NAME,
             # lambda_log_level=LAMBDA_LOG_LEVEL_PER_ENVIRONMENT[ENVIRONMENT_TYPE],

             # If you don't specify 'env', this stack will be environment-agnostic.
             # Account/Region-dependent features and context lookups will not work,
             # but a single synthesized template can be deployed anywhere.

             # Uncomment the next line to specialize this stack for the AWS Account
             # and Region that are implied by the current CLI configuration.

             # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

             # Uncomment the next line if you know exactly what Account and Region you
             # want to deploy the stack to. */

             # env=cdk.Environment(account='123456789012', region='us-east-1'),

             # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
             )

app.synth()
os.remove('.lambda_layers_dependencies/requirements.txt')
