import io
import json
import logging
import random
import time
import zipfile
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def create_lambda_deployment_package(function_file_name):
    """
    Creates a Lambda deployment package in ZIP format in an in-memory buffer. This
    buffer can be passed directly to AWS Lambda when creating the function.
    :param function_file_name: The name of the file that contains the Lambda handler
                               function.
    :return: The deployment package.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipped:
        zipped.write(function_file_name)
    buffer.seek(0)
    return buffer.read()


def create_iam_role_for_lambda(iam_resource, iam_role_name):
    """
    Creates an AWS Identity and Access Management (IAM) role that grants the
    AWS Lambda function basic permission to run. If a role with the specified
    name already exists, it is used for the demo.
    :param iam_resource: The Boto3 IAM resource object.
    :param iam_role_name: The name of the role to create.
    :return: The newly created role.
    """
    lambda_assume_role_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Principal': {
                    'Service': 'lambda.amazonaws.com'
                },
                'Action': 'sts:AssumeRole'
            }
        ]
    }
    policy_arn = 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    #policy_arn = 'arn:aws:iam::137479420152:role/LambdaRole'
    try:
        role = iam_resource.create_role(
            RoleName=iam_role_name,
            AssumeRolePolicyDocument=json.dumps(lambda_assume_role_policy))
        iam_resource.meta.client.get_waiter('role_exists').wait(RoleName=iam_role_name)
        logger.info("Created role %s.", role.name)

        role.attach_policy(PolicyArn=policy_arn)
        logger.info("Attached basic execution policy to role %s.", role.name)
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            role = iam_resource.Role(iam_role_name)
            logger.warning("The role %s already exists. Using it.", iam_role_name)
        else:
            logger.exception(
                "Couldn't create role %s or attach policy %s.",
                iam_role_name, policy_arn)
            raise

    return role


def deploy_lambda_function(
        lambda_client, function_name, handler_name, iam_role, deployment_package):
    """
    Deploys the AWS Lambda function.
    :param lambda_client: The Boto3 AWS Lambda client object.
    :param function_name: The name of the AWS Lambda function.
    :param handler_name: The fully qualified name of the handler function. This
                         must include the file name and the function name.
    :param iam_role: The IAM role to use for the function.
    :param deployment_package: The deployment package that contains the function
                               code in ZIP format.
    :return: The Amazon Resource Name (ARN) of the newly created function.
    """
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Description="AWS Lambda demo",
            Runtime='python3.8',
            Role=iam_role.arn,
            Handler=handler_name,
            Code={'ZipFile': deployment_package},
            Publish=True,
            Region="us-east-1")
        function_arn = response['FunctionArn']
        logger.info("Created function '%s' with ARN: '%s'.",
                    function_name, response['FunctionArn'])
    except ClientError:
        logger.exception("Couldn't create function %s.", function_name)
        raise
    else:
        return function_arn


def usage_demo():
    """
    Shows how to create, invoke, and delete an AWS Lambda function.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    print('-'*88)
    print("Welcome to the AWS Lambda basics demo.")
    print('-'*88)

    lambda_function_filename = 'src/main/Lambdas/mylambda.py'
    lambda_handler_name = 'mylambda.my_handler'
    lambda_role_name = 'jenkins-iam-role'
    lambda_function_name = 'sample-lambda-function'

    iam_resource = boto3.resource('iam')
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    print("Creating AWS Lambda function {lambda_function_name} from the {lambda_handler_name} function in {lambda_function_filename}...")
    deployment_package = create_lambda_deployment_package(lambda_function_filename)
    iam_role = create_iam_role_for_lambda(iam_resource, lambda_role_name)

    fun_arn = deploy_lambda_function(lambda_client,lambda_function_name,lambda_handler_name,iam_role,deployment_package)
    print("Function ARN: "+fun_arn)
    print("function created successfully")


if __name__ == '__main__':
    usage_demo()
