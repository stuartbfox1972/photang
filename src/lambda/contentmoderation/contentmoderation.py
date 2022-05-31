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

def detect_moderation_labels(bucket, key, confidence):
    response = rekognition_client.detect_moderation_labels(Image={"S3Object": 
                                                        {"Bucket": bucket,
                                                         "Name": key}},
                                                MinConfidence=confidence)
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

    response = detect_moderation_labels(bucket, key, 50)
  

    print('Detected labels for ' + key)    
    for label in response['ModerationLabels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        print (label['ParentName'])
    # return len(response['ModerationLabels'])
    value = {"approved": "true"}
    return value