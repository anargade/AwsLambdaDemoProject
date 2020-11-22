"""
Purpose
Shows how to use the AWS SDK for Python (Boto3) to create an AWS Lambda function,
invoke it, and delete it.
"""
import os
import io
import json
import logging
import random
import sys
import time
import zipfile
import boto3
from botocore.exceptions import ClientError
import yaml

logger = logging.getLogger(__name__)
functionName = '';
desc = ''
handler = ''
memory = 0
publish = ''
role = ''
runtime = ''
tags = ''
timeout = 0
name = str(sys.argv[1])
fileName = ''
region = ''
funcFileName = ''

def create_lambda_deployment_package(function_file_name):
    """
    Creates a Lambda deployment package in ZIP format in an in-memory buffer. This
    buffer can be passed directly to AWS Lambda when creating the function.
    :param function_file_name: The name of the file that contains the Lambda handler
                               function.
    :return: The deployment package.
    """
    os.chdir('src/main/Lambdas/'+name)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipped:
        zipped.write(function_file_name, compress_type=zipfile.ZIP_DEFLATED)
        zipped.close()
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
    #               arn:aws:iam::137479420152:role/jenkins-iam-role
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
        lambda_client, function_name, handler_name, iam_role, deployment_package,lambda_runtime,lambda_desc,lambda_publish):
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
            Description=lambda_desc,
            Runtime=lambda_runtime,
            Role=iam_role.arn,
            Handler=handler_name,
            Code={'ZipFile': deployment_package},
            Publish= bool(lambda_publish))
        function_arn = response['FunctionArn']
        logger.info("Created function '%s' with ARN: '%s'.",
                    function_name, response['FunctionArn'])
    except ClientError:
        logger.exception("Couldn't create function %s.", function_name)
        raise
    else:
        return function_arn


def usage_demo():
    filePath = []
    # Read YAML file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print('path: ' + dir_path)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.startswith(name) & file.endswith('.yaml'):
                # filePath.append(os.path.join(str(root), file))
                filePath = str(root) + '/' + str(file)
                fileName = str(file)
                print('File Name: ', fileName)

    print('file path: ' + filePath)
    with open(filePath, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
        # print('yaml_data: ' + yaml_data)

        functionName = yaml_data['FunctionName']
        print('functionName: ' + functionName)
        desc = yaml_data['Description']
        print('desc: ' + desc)
        handler = yaml_data['Handler']
        print('handler: ' + handler)
        memory = str(yaml_data['MemorySize'])
        print('memory: ' + memory)
        publish = str(yaml_data['Publish'])
        print('publish: ' + publish)
        role = str(yaml_data['Role'])
        print('role: ' + role)
        runtime = yaml_data['Runtime']
        print('runtime: ' + runtime)
        tags = str(yaml_data['Tags'])
        print('tags: ' + tags)
        timeout = str(yaml_data['Timeout'])
        print('timeout: ' + timeout)
        region = yaml_data['Region']
        print('region: ' + region)
        funcFileName = yaml_data['FunctionFileName']
        print('funcFileName: '+ funcFileName)

    """
    Shows how to create, invoke, and delete an AWS Lambda function.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    print('-'*88)
    print("Welcome to the AWS Lambda basics demo.")
    print('-'*88)

    lambda_function_filename = funcFileName
    lambda_handler_name = handler
    lambda_role_name = role
    lambda_function_name = functionName
    lambda_runtime = runtime
    lambda_desc = desc
    lambda_publish = publish

    iam_resource = boto3.resource('iam')
    lambda_client = boto3.client('lambda', region)

    print('File Name: '+fileName+' Function Name: ' + functionName + ' Runtime: ' + runtime + ' IamRole: ' + role + ' Handler: ' + handler )
    print(f"Creating AWS Lambda function {lambda_function_name} from the "
          f"{lambda_handler_name} function in {lambda_function_filename}...")
    deployment_package = create_lambda_deployment_package(lambda_function_filename)
    iam_role = create_iam_role_for_lambda(iam_resource, lambda_role_name)

    fun_arn = deploy_lambda_function(lambda_client,lambda_function_name,lambda_handler_name,iam_role,deployment_package,lambda_runtime,lambda_desc,lambda_publish)

    print("Function ARN: "+fun_arn)
    print("function created successfully")

    # 1. FunctionName 2. Runtime 3. IAM Role 4. Handler 5. Code (zipFile) will be created on the fly  6. env

if __name__ == '__main__':
    usage_demo()
