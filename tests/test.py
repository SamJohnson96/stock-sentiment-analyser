import imp
import requests
import json
import sys
import boto3
import botocore
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('results')
pk_name = 'article_id'
response = table.get_item(Key={pk_name: 10})

if 'Item' in response.keys():
    print ('True')
else:
    print ('False')
