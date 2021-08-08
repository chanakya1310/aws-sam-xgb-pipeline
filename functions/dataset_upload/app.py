import boto3
import random
import csv
import json
import pandas as pd

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    base_key = 'xgb-pipeline/'

    data = pd.read_csv('iris.csv')
    column_names = ["species", "sepal_length", "sepal_width", 'petal_length', 'petal_width']
    data = data.reindex(columns=column_names)  #SageMaker Training job requires first column as label
    data = data.sample(frac=1)
    train = data[0:120]
    test = data[120:]
    train = train.values.tolist()
    test = test.values.tolist()
    bucket_name = 'aws-sam-cli-managed-default-samclisourcebucket-1r9b55q24oemy'
    bucket = s3.Bucket(bucket_name)

    with open('/tmp/train.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(train)

    with open('/tmp/test.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(test)

    bucket.upload_file('/tmp/train.csv', base_key + 'train.csv')
    bucket.upload_file('/tmp/test.csv', base_key + 'test.csv')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'train': base_key + 'train.csv',
            'test': base_key + 'test.csv'
        })
    }