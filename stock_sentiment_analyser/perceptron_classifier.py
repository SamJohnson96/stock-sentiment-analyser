import glob
import pandas as pd
import numpy as np
from newspaper import Article
from sklearn import datasets
from sklearn.linear_model import Perceptron


def import_training_dataframe():
    path_to_dataframe = local_path + 'training_set.pickle'
    return pd.read_pickle(path_to_dataframe)

def remove_duplicates(complete_word_list):
    return set((item for item in complete_word_list))

def get_vector_keyword_index(article_contents):
    complete_word_list = [item for sublist in article_contents for item in sublist]
    unique_word_list = remove_duplicates(complete_word_list)
    vector_index={}
    offset=0
    #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
    for word in unique_word_list:
            vector_index[word] = offset
            offset+=1
    return vector_index

def make_vector(article_content,vector_keyword_index):
    vector = [0] * len(vector_keyword_index)
    for word in article_content:
            vector[vector_keyword_index[word]] += 1; #Use simple Term Count Model
    return vector


local_path = '/Users/sam/Desktop/GDELT_Data/'

# Get training data
training_data = import_training_dataframe()

# Split dataframe into 75 training / 25 testing
articles = training_data['article_content']
vectors = training_data['article_vector']
classification = training_data['classification']

#Create our vector_keyword_index
vector_keyword_index = get_vector_keyword_index(articles)

#Create our training sample
train_sample = training_data[0:100]
train_data = train_sample['article_vector']
train_answers = train_sample['classification']
train_data = np.matrix(train_data.tolist())

#Create our test sample
test_sample = training_data[101:144]
test_data = test_sample['article_vector']
test_answers = test_sample['classification']
test_data = np.matrix(test_data.tolist())
test_answers = test_answers.as_matrix()

#Perceptron
perceptron = Perceptron()
perceptron.fit(train_data, train_answers)

#Test
results = []
for row in test_data:
    results.append(perceptron.predict(row))

correct = 0
wrong = 0
for x in range(0,42):
    if results[x] == test_answers[x]:
        correct += 1
    else:
        wrong += 1

print float(correct)/(float(wrong)+float(correct))
