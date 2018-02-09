import nltk as nltk
import numpy as np
import sys
import logging
import pymysql
from nltk import word_tokenize
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

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

    # Run model :)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set)) # test accuracy is 0.753101551116

# Get random data
def get_rand_training_data():
    item_count = 0
    rows = []
    with conn.cursor() as cur:
        cur.execute('insert into users (name) values("Joe")')
        conn.commit()
        cur.execute("SELECT * FROM articles AS r1 JOIN (SELECT CEIL(RAND() * (SELECT MAX(id) FROM articles)) AS id) AS r2 WHERE r1.id >= r2.id ORDER BY r1.id ASC LIMIT 50")
        for row in cur:
            rows.append(row)
    return rows

# Remove those duplicate words from word vector list
def remove_duplicate_words(complete_word_list):
    return set((item for item in complete_word_list))

# Create a whole vectory keyword index based on the given training data
def create_vector_keyword_index(training_data):
    # take training data and get contents of each article and place into another array
    training_data_article_contents = [item[2] for item in training_data]
    split_articles_list = split_articles(training_data_article_contents)
    complete_word_list = [item for sublist in split_articles_list for item in sublist]
    unique_word_list = remove_duplicate_words(complete_word_list)
    vector_index = {}
    offset = 0

    # Associate a position with the keywords which maps to the dimension on the vector used to represent this word
    for word in unique_word_list:
        vector_index[word] = offset
        offset += 1
    return vector_index

# Method that takes an array of article contents and returns an array of each article split into array
def split_articles(article_contents):
    split_articles = []
    for article in article_contents:
        article = article.split()
        split_articles.append(article)
    return split_articles

def make_feature_set(training_data, vector_keyword_index):
    # Get articles of training_data
    training_data_article_contents = [item[2] for item in training_data]
    # Split the contents of each article content
    split_articles_list = split_articles(training_data_article_contents)

    args = []
    results = []
    feature_set = []

    for article in split_articles_list:
        args.append(make_vector(article,vector_keyword_index))

    for training in training_data:
        if training[3] > 0:
            results.append(1)
        else:
            results.append(0)

    for x in range(len(training_data)):
        feature_tuple = (args[x],results[x]);
        feature_set.append(feature_tuple)

    return feature_set


def make_vector(article_content, vector_keyword_index):
    # Run through each word in train_data
    vector = {}
    # Create dictionary with vector_keyword_index
    for word in vector_keyword_index:
        vector[word] = 0

    for word in article_content:
            vector[word] += 1; #Use simple Term Count Model
    return vector


# Download training_data - An tuple [0] - id [1] - source_url [2] - preprocessed_content [3] - avg_tone
training_data = get_rand_training_data()

# Create keyword_index dictionary
vector_keyword_index = create_vector_keyword_index(training_data)

# Give every article their own vector index
training_data = make_feature_set(training_data, vector_keyword_index)

# From the 'master' feature list, split it into test and training
train_set, test_set = train_test_split(training_data, test_size = 0.2, random_state=128)

# Run model :)
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
