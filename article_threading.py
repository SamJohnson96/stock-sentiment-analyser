import threading
import time
from models.article import Article
from newspaper import Article as newspaper_article
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def download_article(article, article_array):
    print article
    print 'Downloading %s' %article[0]
    a = newspaper_article(article[0])
    a.download()
    a.parse()
    text = a.text.encode('utf-8')
    preprocessed_text = preprocess_article_content(text)
    processed_content = " "
    article_object = Article(
                        source_url = article[0],
                        content = processed_content.join(preprocessed_text),
                        avg_tone = article[1]
                    )
    article_array.append(article_object)

    print 'Thread finished'

def clean(article):
    article = article.replace(".", "")
    article = article.replace("\s+", " ")
    article = article.lower()
    return article

def remove_stop_words(article):
    stop_words = set(stopwords.words('english'))
    return [word for word in article if word not in stop_words]

def tokenize(article):
    ps = PorterStemmer()
    string = clean(article)
    words = string.split(" ")
    return [ps.stem(word) for word in words]

def preprocess_article_content(article_contents):
    return remove_stop_words(tokenize(article_contents))

def process_threads(filtered_articles):
    jobs = []
    res = []
    for article_list in filtered_articles:
        for article in article_list:
            thread = threading.Thread(target=download_article, kwargs={'article': article, 'article_array' : res})
            thread.daemon=True
            jobs.append(thread)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    return res
