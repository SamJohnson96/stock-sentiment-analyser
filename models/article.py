from .database_tools import Base
from sqlalchemy import Column, Integer, String, Float, Text

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    source_url = Column(Text)
    content = Column(Text)
    avg_tone = Column(Float)
