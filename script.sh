#!/bin/bash
 
FUNCTION_NAME=$1

zip -r $FUNCTION_NAME.zip src/main/Lambdas/

aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "python2.7" \
        --zip-file "fileb://.src/main/Lambdas/$FUNCTION_NAME.zip" \
        --handler "src/main/Lambdas/mylambda.my_handler" \
        --role "arn:aws:iam::137479420152:role/aws-lambda-demo-role" \
        --timeout 3 \
        --region "us-east-1"
 
echo "$FUNCTION_NAME"
