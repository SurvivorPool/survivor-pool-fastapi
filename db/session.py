import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv('.env')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
