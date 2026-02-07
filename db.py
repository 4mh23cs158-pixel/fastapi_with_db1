from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
Base = declarative_base()
from dotenv import load_dotenv
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL ahhah", DATABASE_URL)
# create engine once at module level
engine = create_engine(DATABASE_URL)

# create sessionmaker class for creating database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()