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

    print(article_topic)
    # Check to see if we need to carry on with classification.
    if (article_topic != 'facebook') and (article_topic != 'apple') and (article_topic != 'technology'):
        print ('article not to be classified')
        return;

    classification = classify_new_article(article_content);

    print (classification)

    if classification is not None:
        print('---- Updating row into parsed_articles ----')
        update_row(article_id,article_topic,classification)
        print('---- Done ----')

def classify_new_article(article_content):
    url = "http://ec2-35-177-151-51.eu-west-2.compute.amazonaws.com/classify-linear"
    headers = {'Content-Type': 'application/json'}
    article_json = {"Article":{"content":article_content}}
    response = requests.post(url, headers=headers, json=article_json)
    if response.status_code == 200:
        return response.content
    else:
        print ('error occured during api called')
        return None

# Update row into Dynamodb table
def update_row(article_id,article_topic,classification):
    time.sleep(3)
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
        UpdateExpression='SET linear_perceptron = :val1',
        ExpressionAttributeValues={
            ':val1': str(classification, 'utf-8')
        }
    )
