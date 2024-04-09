from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

#sqlalchemy model is for defining the columns of our tables

"""
sqlalchemy Limitation:
1. it will create tables as per below details if the table don't exists in db. 
2. If table already exists, then it will not make any changes
3. To achive this we need to use Alembic tool (kind of data migration tool)

"""

class Post(Base):
    __tablename__ ="posts"

    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, nullable= False, server_default= 'TRUE')
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable= False)

    #this is not related db , 
    #it maintians the relationship for response property and does auto join and bring the infor required
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    id = Column(Integer, primary_key= True, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, 
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key= True, 
                     nullable= False)
    user_id = Column(Integer, 
                     ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key= True, 
                     nullable= False)