from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
 
import settings
 
DeclarativeBase = declarative_base()
 
def db_connect():
    return create_engine(URL(**settings.DATABASE))
 
def create_crawler_table(engine):
    DeclarativeBase.metadata.create_all(engine)
 
class Crawler(DeclarativeBase):
    __tablename__ = "crawler"
 
    id = Column(Integer, primary_key=True)
    title = Column('title', String(200))
    link = Column('link', String(200))
