from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_DIALECT=os.getenv("DB_DIALECT")
DB_DRIVER=os.getenv("DB_DRIVER")
DB_USER=os.getenv("DB_USER")
DB_PASSWD=os.getenv("DB_PASSWD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_URL = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
print(DB_URL)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()