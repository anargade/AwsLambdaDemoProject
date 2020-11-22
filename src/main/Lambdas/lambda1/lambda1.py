import json
import os
import yaml
def my_handler(event, context):
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

    with open(filePath, 'r') as stream:
        yaml_data = yaml.safe_load(stream)
        username = yaml_data['username']
        print('username: ' + username)
        url = yaml_data['url']
        print('url: ' + url)
    return {
        'statusCode': 200,
        'username': username,
        'url': url,
        'body': json.dumps('Hello from Lambda1')
    }
