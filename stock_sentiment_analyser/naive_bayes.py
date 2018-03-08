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
            article_id = record['dynamodb']['NewImage']['article_id']['N']
            article_content = record['dynamodb']['NewImage']['article_content']['S']
            article_topic = record['dynamodb']['NewImage']['classification']['S']
        else:
            print('No article to scrape')
            return;
    print('---- Parsing article ----')

    # Check to see if we need to carry on with classification.
    if (article_topic != 'facebook') or (article_topic != 'apple') or (article_topic != 't'):
        print ('article not to be classified')
        return;

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

def check_if_article_exists(article_id,article_topic):
    dynamodb = boto3.resource('dynamodb')
    if article_topic == 'facebook':
        table = dynamodb.Table('facebook_article_results')
    elif article_topic == 'apple':
        table = dynamodb.Table('apple_article_results')
    elif article_topic == 'technology':
        table = dynamodb.Table('technology_article_results')

    pk_key = 'article_id'
    response = table.get_item(Key={pk_key: int(article_id)})
    if 'Item' in response.keys():
        return True
    else:
        return False

# Insert row into Dynamodb table
def insert_row(article_id,article_content,article_topic,classification):
    print('--- inserting row ---')
    dynamodb = boto3.resource('dynamodb')
    if article_topic == 'facebook':
        table = dynamodb.Table('facebook_article_results')
    elif article_topic == 'apple':
        table = dynamodb.Table('apple_article_results')
    elif article_topic == 'technology':
        table = dynamodb.Table('technology_article_results')

    table.put_item(
        Item={
            'article_id' :  int(article_id),
            'naive_bayes_classification' : str(classification, 'utf-8')
        }
    )

# Update row into Dynamodb table
def update_row(article_id,article_topic,classification):
    print('--- updating row ---')
    dynamodb = boto3.resource('dynamodb')
    if article_topic == 'facebook':
        table = dynamodb.Table('facebook_article_results')
    elif article_topic == 'apple':
        table = dynamodb.Table('apple_article_results')
    elif article_topic == 'technology':
        table = dynamodb.Table('technology_article_results')

    table.update_item(
    Key={
        'article_id': int(article_id),
    },
    UpdateExpression='SET naive_bayes_classification = :val1',
    ExpressionAttributeValues={
        ':val1': str(classification, 'utf-8')
    }
)
