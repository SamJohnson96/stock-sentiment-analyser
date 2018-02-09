#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import article_threading
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

    print('--- Creating article arrays ---')
    # Create article arrays
    downloaded_articles = []
    for name in csv_names:
        downloaded_articles.append(db_csv_tools.scrape_csv_file(local_path,name))
    print('--- Done ---')

    print('--- Removing duplicate URLs ---')
    filtered_articles = [
        db_csv_tools.filter_out_duplicates(article_list)
        for article_list in downloaded_articles
    ]

    print('--- Done ---')

    # Create Article models
    return article_threading.process_threads(filtered_articles)


def parse_latest_csv(local_path = '/Users/sam/Desktop/'):
    db_csv_tools.find_latest_csv()


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
