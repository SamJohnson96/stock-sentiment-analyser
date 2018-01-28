import glob
import csv
import numpy as np
import MySQLdb
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from newspaper import Article
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from os import listdir


def find_csv_filenames(path_to_dir, suffix=".export.CSV"):
    """Method that retrieves the all the CSV file names that have been downloaded from GDELT in a given location

    Args:
        path_to_dir (string): The location of the downloaded GDELT csv files.
        suffix(string): The suffix of the file names.

    Returns:
        array: Array of filenames found in the list.

    """
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def scrape_csv_file(path_to_csv, csv_filename):
    """Method that goes through a GDELT CSV file and extracts information from each row

    Args:
        path_to_csv (string): The location of the downloaded GDELT csv file.
        csv_filename(string): The filename that is being looked for in the directory.

    Returns:
        array: Array of selected fields from each row.

    """
    with open(path_to_csv + csv_filename) as csvfile:
        print 'reading ' + csv_filename
        readCSV = csv.reader(csvfile, delimiter='\t')
        articles = []
        for row in readCSV:
            source_url = row [57]
            avg_tone = row [34]
            articles.append([source_url, avg_tone])

        return articles


def filter_out_duplicates(csv_list):
    """Method that removes duplicate URLs from scraped csv files.

    Args:
        csv_list (string): List of CSV objects that were created.

    Returns:
        array: Array of non duplicate urls.

    """
    url_list = []
    filtered_csv = []
    for csv in csv_list:
        if csv[0] not in url_list:
            url_list.append(csv[0])
            filtered_csv.append(csv)
    return filtered_csv

def get_article_content(url):
    """Method that downloads the article content of a given url

    Args:
        url (string): URL to download

    Returns:
        array: content of the article

    """
    a = Article(url)
    a.download()
    a.parse()
    return a.text.encode('utf-8')

def clean(article):
    article = article.replace(".", "")
    article = article.replace("\s+", " ")
    article = article.lower()
    return article

def remove_stop_words(article):
    return [word for word in article if word not in stop_words]

# Update to use INFJ
def tokenize(article):
    string = clean(article)
    words = string.split(" ")
    return [ps.stem(word) for word in words]

def preprocess_article_content(article_contents):
    return remove_stop_words(tokenize(article_contents))

def remove_duplicates(complete_word_list):
    return set((item for item in complete_word_list))

def get_vector_keyword_index(article_contents):
    complete_word_list = [item for sublist in article_contents for item in sublist]
    unique_word_list = remove_duplicates(complete_word_list)
    vector_index = {}
    offset = 0
    # Associate a position with the keywords which maps to the dimension on the vector used to represent this word
    for word in unique_word_list:
        vector_index[word] = offset
        offset += 1
    return vector_index

def make_vector(article_content, vector_keyword_index):
    vector = [0] * len(vector_keyword_index)
    for word in article_content:
        vector[vector_keyword_index[word]] += 1  # Use simple Term Count Model
    return vector

#
# # Get directory where CSVs are held.
# local_path = '/Users/sam/Desktop/GDELT_Data/tmp/'
# csv_names = find_csv_filenames(local_path)
#
# # Create article objects
# downloaded_articles = []
# for name in csv_names:
#     downloaded_articles.append(scrape_csv_file(local_path,name))
#
# # Filter out duplicate
# filtered_articles = filter_out_duplicates(downloaded_articles)
#
# # Now to download articles and preprocess
# articles = []
# for article in filtered_articles:
#     article = []
#     article.append(preprocess_article_content(get_article_content(article[0])))
#     article.append(article[1])
#     articles.append(article)






#
# # NLTK extensions
# ps = PorterStemmer()
# stop_words = set(stopwords.words('english'))
#
#
# # Tokenize and remove stop words from every article
# article_contents = []
# article_classification = []
# for index, row in dataframe.iterrows():
#     print row
#     article_contents.append(preprocess_article_content(get_article_content(row['SOURCEURL'])))
#     article_classification.append(classify_article(row['AvgTone']))
#
# # Create vector keyword index
# vector_keyword_index = get_vector_keyword_index(article_contents)
#
# # Create vector for each article
# article_vectors = []
# for content in article_contents:
#     article_vectors.append(make_vector(content, vector_keyword_index))
#
# # Update dataframe
# training_set = create_dataframe(article_contents, article_vectors, article_classification)
#
# training_set.to_pickle(local_path + 'training_set.pickle')
