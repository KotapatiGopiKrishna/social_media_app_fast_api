from fastapi import HTTPException, status,Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users'] #to group webservices in the documentation
)

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user( user : schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    #convert the request to db query
    new_user = models.User(**user.model_dump())

    #adding to db
    db.add(new_user)
    #commit to db
    db.commit()
    #return the newly create post
    db.refresh(new_user)
    
    return new_user

@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"user with id: {id} doesn't not exist")
    
    return user