import boto3
import json
import os

def lambda_handler(event, context):
  sfn_client = boto3.client('stepfunctions')
  state_machine_arn = os.environ['STEP_FUNCTION_ARN']

  response = sfn_client.start_execution(
    stateMachineArn=state_machine_arn,
    name='test1',
    input=json.dumps({ 'TransactionType': 'PURCHASE' })
  )

  print(response)