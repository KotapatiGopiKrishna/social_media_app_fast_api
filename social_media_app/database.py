import psycopg2
from psycopg2.extras import RealDictCursor
import time


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#Create a database URL for SQLAlchemy
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:Welcome1234@localhost/social_media_fastapi'
#SQL_ALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ipaddress/hostname>/<databasename>'

#Create a SQLAlchemy engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

#Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

#create a Base class
Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#database connection before using ORM, will be commented after implementing ORM
#not using
'''
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='social_media_fastapi', user= 'postgres', password= 'Welcome1234', cursor_factory= RealDictCursor )
        cursor = conn.cursor()
        print("Database connection wass sucessful!")
        break
    except Exception as error:
        print("Connection was failed")
        print("Error: ", error)
        time.sleep(2)'''