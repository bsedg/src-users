# Import the necessary classes from the AWS CDK package
from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
)

###
### Run with commands:
# $ cdk synth
# $ cdk deploy
###

# Define a new CDK stack
class MyStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        # Define the Lambda function that will handle incoming API requests
        my_lambda = lambda_.Function(
            self,
            "MyLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=lambda_.Code.asset("lambda_function_code"),
        )

        # Define the DynamoDB table that the Lambda function will read from
        my_table = dynamodb.Table(
            self,
            "MyTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
        )

        # Give the Lambda function permission to read from the DynamoDB table
        my_table.grant_read_data(my_lambda)

        # Define the SQS queue that the Lambda function will write to
        my_queue = sqs.Queue(self, "MyQueue")

        # Give the Lambda function permission to write to the SQS queue
        my_queue.grant_send_messages(my_lambda)

        # Define the API Gateway that will trigger the Lambda function
        api = apigateway.LambdaRestApi(
            self,
            "MyApi",
            handler=my_lambda,
        )
