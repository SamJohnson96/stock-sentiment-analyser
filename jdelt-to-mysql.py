#!/usr/bin/env python
import argparse
from scripts import db_csv_tools
from models.article import Article
from models.database_tools import Base, create_all_tables, create_new_engine, setup_database, create_new_session
from sqlalchemy import Column, Integer, String, Float


def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="process all CSV files",
                    action="store_true")
    return parser

def parse_all_csv(local_path = '/Users/sam/Desktop/'):
    # csv_names = [db_csv_tools.find_csv_filenames(local_path)[0]]
    csv_names = ['training_data.csv']

    # Create article arrays
    downloaded_articles = []
    for name in csv_names:
        downloaded_articles.append(db_csv_tools.scrape_csv_file(local_path,name))

    filtered_articles = [
        db_csv_tools.filter_out_duplicates(article_list)
        for article_list in downloaded_articles
    ]
    print(len(downloaded_articles[0]))

    # Create article models
    articles = []
    for article_list in filtered_articles:
        print(len(article_list))
        for article in article_list:
            reduced_article = Article(
                source_url = article[0],
                content = db_csv_tools.get_article_content(article[0]),
                avg_tone = article[1]
            )
            articles.append(reduced_article)
    return articles


if __name__ == "__main__":
    parser = build_args()
    args = parser.parse_args()
    engine = create_new_engine('stockbot')
    if args.all:
        articles = parse_all_csv()
    else:
        articles = parse_latest_csv()

    Session = create_new_session(engine)
    session = Session()
    session.bulk_save_objects(articles)
    session.commit()
