from database_tools import Base, create_new_engine

def create_all_tables(engine):
  Base.metadata.create_all(engine)
