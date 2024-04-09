from datetime import datetime
from typing import Optional

#pydantic models are used to validate the formate of payload
from pydantic import BaseModel, ConfigDict, EmailStr, conint

#schema / pydantic model : to control the type of request and request validaitons
#----API request models ----
class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr #this will work only if we have email-validator installed and automatically checks
    password: str

class UserLogin(BaseModel):
    email: EmailStr #this will work only if we have email-validator installed and automatically checks
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    #
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # this will validate values as well

#----API response models ----
class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime
    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut #continuation to changes in models relationship functionality

    '''class Config:
        orm_mode = True'''
    

class PostOut(BaseModel):
    Post: Post
    votes: int

    
