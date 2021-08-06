import boto3
import random
import csv
import json

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    base_key = 'csv/'

    train_points = [(random.randint(RANGE_BEGIN, RANGE_END), random.randint(RANGE_BEGIN, RANGE_END)) for i in range(NUM_EXAMPLES)]
    train = [[f(x, y), x, y] for x, y in train_points]
    test = [[random.randint(RANGE_BEGIN, RANGE_END), random.randint(RANGE_BEGIN, RANGE_END)] for i in range(NUM_EXAMPLES)]
    bucket_name = 'stepfunctionssample-sagemak-bucketformodelanddata-1bby5at6z2xhv'
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