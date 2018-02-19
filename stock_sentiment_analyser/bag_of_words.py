import pandas as pd
import nltk as nltk
import numpy as np
import sys
import logging
import pymysql
from nltk import word_tokenize
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

#rds settings
rds_host  = "stockbot.c0mj2r8tlwe3.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "mypassword"
db_name = "stockbot"

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    # logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

# logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def lambda_handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    # Download training_data - An tuple [0] - id [1] - source_url [2] - preprocessed_content [3] - avg_tone
    training_data = get_rand_training_data()

    # Create keyword_index dictionary
    vector_keyword_index = create_vector_keyword_index(training_data)

    # Give every article their own vector index
    training_data = make_feature_set(training_data, vector_keyword_index)

    # From the 'master' feature list, split it into test and training
    train_set, test_set = train_test_split(training_data, test_size = 0.2, random_state=128)
    #TODO: DEAL WITH AMAZON AWS EVENT

    # Run model :)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set)) # test accuracy is 0.753101551116

# Get random data
def get_rand_training_data():
    item_count = 0
    rows = []
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM articles AS r1 JOIN (SELECT CEIL(RAND() * (SELECT MAX(id) FROM articles)) AS id) AS r2 WHERE r1.id >= r2.id ORDER BY r1.id ASC LIMIT 100")
        for row in cur:
            rows.append(row)
    return rows

def create_training_dataframe(training_data):
    """Method that merges all 3 training sets into one dataframe

    Args:
        merged_training (Array): Array of articles to place into dataframe

    Returns:
        dataframe: Organised dataframe of all training data

    """
    classified_data = []
    for article in training_data:
        if article[4] < 0:
            article = article + (0,)
        else:
            article = article + (1,)
        classified_data.append(article)

    df = pd.DataFrame(classified_data)
    df.columns = ['db_id', 'source_url', 'headline', 'content', 'avg_tone', 'category','added_field','tone']
    return df

def run_validation_tests(training_data):
    # Split the training_data into two
    train, test = train_test_split(training_data, test_size=0.1)
    # Run pipeline and get predictions
    prediction = run_pipeline(train, test)
    
    print (prediction)



def run_pipeline(training_data,testing_dataframe):
    """Method that takes an array of training articles and returns them into an organised dataframe

    Args:
        articles (Array): Array of articles to place into dataframe

    Returns:
        dataframe: Organised dataframe of all training data

    """
    # Create pipline
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                        ])

    # Fit and do validation test
    text_clf = text_clf.fit(training_data.content, training_data.tone)
    predicted = text_clf.predict(testing_dataframe.headline)
    return predicted

# Training_data
training_data = get_rand_training_data()
# Create dataframe from Training_data
training_data = create_training_dataframe(training_data)
# Validation tests
run_validation_tests(training_data)
