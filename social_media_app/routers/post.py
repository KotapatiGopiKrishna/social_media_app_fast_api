from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # to group webservices in the documentation
)

# to get the data from the list instead of database example
# my_posts = [{"title" : "title of post 1" , "content" : "Content of post 1","id" : 1}, {"title" : "title of post 2" , "content" : "Content of post 2","id" : 2}]

'''def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i'''


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,  # to limit the number of results from params
              skip: int = 0,  # to Skip some of results from params
              # to give search feability from params
              search: Optional[str] = ""
              ):
    # to select data using database connection and sql , dependecy  in parameter section is not required for this method
    '''cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()'''

    # to select data using ORM
    # from one table
    '''posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()'''

    # from multiple tables with joins
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.get("/loggeduser", response_model=List[schemas.PostOut])
def get_posts_by_loggedin_owner(db: Session = Depends(get_db),
                                current_user: int = Depends(
                                    oauth2.get_current_user),
                                limit: int = 10):
    # to select data using database connection and sql , dependecy  in parameter section is not required for this method
    '''cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()'''

    # to select data using ORM
    '''posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id).all()'''

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id).all()

    return results


@router.get("/latest", response_model=schemas.PostOut)
def get_latest_post(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    '''post = my_posts[len(my_posts) - 1 ]
    return {"data": post}'''

    # to get data using database connection & sql,  dependecy  in parameter section is not required for this method
    '''cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    post = cursor.fetchone()'''

    # -- to create data using ORM
    '''post = db.query(models.Post).filter(models.Post.owner_id ==
                                        current_user.id).order_by(models.Post.id.desc()).first()'''

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.owner_id == current_user.id).order_by(models.Post.id.desc()).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # to get data using array/list
    '''post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found"
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post with id: {id} was not found"}
    return {"data": post}'''

    # to get data using database connection & sql,  dependecy  in parameter section is not required for this method
    '''cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    return '''

    # -- to create data using ORM
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    '''print(post.published)
    print(post.rating)
    print(post.model_dump())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000000)
    my_posts.append(post_dict)
    return {"new_post" : post_dict }'''

    # to insert data using database connection and sql, dependecy  in parameter section is not required for this method
    '''cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()'''

    # -- to create data using ORM

    # typical way to set column but it will be hard it we have too many columns it will be too much
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)

    # alternative for above line is
    # owner id is being auto set by logged in user
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    # adding to db
    db.add(new_post)
    # commit to db
    db.commit()
    # return the newly create post
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} doesn't not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)'''

    # to delete data using database connection & sql,  dependecy  in parameter section is not required for this method
    '''cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()'''

    # -- to create data using ORM
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_post_query.first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # verifying whether post is actually created by logged in user
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return deleted_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} doesn't not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict 
    return f"post with id: {id} is updated"'''

    # to upadate data using database connection & sql,  dependecy  in parameter section is not required for this method
    '''cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    return {"data": updated_post}
    '''

    # -- to update data using ORM
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = updated_post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't not exist")
   
    # verifying whether post is actually created by logged in user
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    updated_post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return updated_post
