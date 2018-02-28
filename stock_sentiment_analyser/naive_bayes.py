import imp
import requests
import json
import sys
import boto3
import botocore
import time
from datetime import datetime

def lambda_handler(event, context):
    for record in event['Records']:
        if 'NewImage' in record['dynamodb']:
            article_content = record['dynamodb']['NewImage']['article_content']['S']
            article_id = record['dynamodb']['NewImage']['article_id']['N']
        else:
            print('No article to scrape')
            return;
    print('---- Parsing article ----')
    classification = classify_new_article(article_content);

    if classification is not None:
        print('---- Inserting/Updating row into parsed_articles ----')
        # Need to check if key exists
        if check_if_article_exists(article_id):
            # Update row
            update_row(article_id,classification)
        else:
            #Insert into dynamoDb
            insert_row(article_id,article_content,classification);
        print('---- Done ----')

def classify_new_article(article_content):
    url = "https://2uaz4gpeyh.execute-api.eu-west-2.amazonaws.com/production/naive-bayes"
    headers = {'Content-Type': 'application/json'}
    article_json = {"Article":{"content":article_content}}
    response = requests.post(url, headers=headers, json=article_json)
    if response.status_code == 200:
        return response.content
    else:
        print ('error occured during api called')
        return None

def check_if_article_exists(article_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('results')
    pk_key = 'article_id'
    response = table.get_item(Key={pk_key: int(article_id)})
    if 'Item' in response.keys():
        return True
    else:
        return False

# Insert row into Dynamodb table processed_articles
def insert_row(article_id,article_content,classification):
    print('--- inserting row ---')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('results')
    table.put_item(
        Item={
            'article_id' :  int(article_id),
            'naive_bayes_classification' : str(classification, 'utf-8')
        }
    )

def update_row(article_id,classification):
    print('--- updating row ---')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('results')
    table.update_item(
    Key={
        'article_id': int(article_id),
    },
    UpdateExpression='SET naive_bayes_classification = :val1',
    ExpressionAttributeValues={
        ':val1': str(classification, 'utf-8')
    }
)
