from __future__ import print_function
from decimal import Decimal

import boto3
import datetime
import json
import os
import urllib
import uuid
import time

# --------------- Main handler ------------------
def lambda_handler(event, context):
    return '{"allowed": "true"}'