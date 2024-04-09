from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from social_media_app import models

from . import schemas, database
from .config import settings

#3 items needed
#SECRET_KEY
#Algorithm used to generate the key
#expirition time of the token

#random long string as secret key for testing
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    #set the expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    #create a token
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id") # based on oauth2.py file logic 

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id= id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(OAuth2_scheme) ,db: Session = Depends(database.get_db) ):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail= "Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    
    token = verify_access_token(token, credentials_exception)

    #validate the id receveid from token_data to database, not required you can directly return token
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
