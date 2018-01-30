import threading
import time
from models.article import Article
from newspaper import Article as newspaper_article

def download_article(article, article_array):
    print 'Downloading %s' %article[0]
    a = newspaper_article(article[0])
    a.download()
    a.parse()
    text = a.text.encode('utf-8')
    article_object = Article(
                        source_url = article[0],
                        content = text,
                        avg_tone = article[1]
                    )
    article_array.append(article_object)
    print 'Thread finished'


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
