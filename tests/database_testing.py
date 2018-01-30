#!/usr/bin/env python
from database_tools import Base, create_all_tables, create_new_engine, setup_database, create_new_session
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))


if __name__ == "__main__":
    engine = create_new_engine()
    setup_database(engine, 'stockbot')
    create_all_tables(base, engine)
    user = User(name='ted')
    Session = create_new_session(engine)
    session = Session()
    session.add(user)
    our_user = session.query(User).filter_by(name='sam').first()
    print our_user
