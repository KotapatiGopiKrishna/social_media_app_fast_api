from fastapi import HTTPException, status,Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils, oauth2

router = APIRouter(tags= ['Authentication'])

@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session= Depends(database.get_db)):

    #since we are using OAuth2PasswordRequestForm it will return only username and password
    '''sample of oauth response by default
        {
        "username" : "wewe",
        "password" : "pwdwdwdw"
                }
    '''
    #it will not return as per our pydantic model
    #after enabling the OAuth2PasswordRequestForm credentials must be passed to form data format not raw of the body
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    #verify user email address
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Invalid Credentials')
    
    #verify password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail = "Invalid Credentials" )
    
    #create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    #return token
    return {'access_token': access_token, "token_type": "bearer"}