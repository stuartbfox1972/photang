from __future__ import print_function
from PIL import Image
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
      return {"success": "true"}
    except Exception as e:
        #print("Error processing object {} from bucket {}. Event {}".format(key, bucket, json.dumps(event, indent=2)))
        print(e)
