# !/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_stacks.sidikey_stack import SidikeyStack
import subprocess


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
