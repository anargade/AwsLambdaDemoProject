import json
import os

def my_handler(event, context):
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda1')
    }
