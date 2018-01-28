import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

def create_new_engine(database):
    return create_engine("mysql://admin:mypassword@stockbot.c0mj2r8tlwe3.eu-west-2.rds.amazonaws.com/%s" % database)

def create_all_tables(base, engine):
    Base.metadata.create_all(engine)

def setup_database(engine, database):
    engine.execute("CREATE DATABASE IF NOT EXISTS %s" % database)
    engine.execute("USE %s" % database)

def create_new_session(engine):
    return sessionmaker(bind=engine)
