import article_threading


articles = []
article = [['https://techcrunch.com/2018/01/28/how-publishers-will-survive-facebooks-newsfeed-change/', '0.387350871538985']]
articles.append(article)


results = article_threading.process_threads(articles)

result = results[0]

print type(result.content)
