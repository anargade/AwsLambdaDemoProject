import json
import os
import yaml
def my_handler(event, context):
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda1')
    }
