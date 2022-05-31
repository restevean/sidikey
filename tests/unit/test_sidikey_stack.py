import aws_cdk as core
import aws_cdk.assertions as assertions

from sidikey.sidikey_stack import SidikeyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sidikey/sidikey_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SidikeyStack(app, "sidikey")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
