from __future__ import print_function
from decimal import Decimal

import boto3
import datetime
import json
import os
import urllib
import uuid
import time


rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')
dynamo_client = boto3.client('dynamodb')

# Get the table name from the Lambda Environment Variable
table_name = os.environ['TABLE_NAME']

# --------------- Helper Functions to call Rekognition APIs ------------------

def detect_text(bucket, key):
    response = rekognition_client.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response

def detect_labels(bucket, key, confidence, labels):
    response = rekognition_client.detect_labels(Image={"S3Object": 
                                                        {"Bucket": bucket,
                                                         "Name": key}},
                                                MinConfidence=confidence,
                                                MaxLabels=labels)
    return response

# --------------- Main handler ------------------
def lambda_handler(event, context):
    '''
    Uses Rekognition APIs to detect text and labels for objects uploaded to S3
    and store the content in DynamoDB.
    '''

    # Get the object from the event.
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        # Call rekognition DetectLabels API to detect labels in S3 object.
        response = detect_labels(bucket, key, 90, 10)
        xlabels = []
        labels = []
        
        for label_prediction in response['Labels']:
             xlabels.append(label_prediction['Name'])
             labels.append({label_prediction['Name']: Decimal(str(label_prediction['Confidence']))})

        # Get the timestamp.
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Write to DynamoDB.
        table = boto3.resource('dynamodb').Table(table_name)
        item={'SK': 'IMAGE#' + key, 'PK': 'USER#' + 'DEMO', 'Labels':labels, 'Timestamp':timestamp}
        table.put_item(Item=item)
        with table.batch_writer() as batch:
            for rl in xlabels:
                batch.put_item(
                    Item={'PK': 'LABEL#' + rl, 'SK': 'IMAGE#' + key}
                )

        return 'Success'
    except Exception as e:
        #print("Error processing object {} from bucket {}. Event {}".format(key, bucket, json.dumps(event, indent=2)))
        print(e)
