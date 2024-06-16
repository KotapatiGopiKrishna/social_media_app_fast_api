#fistures in this will be accessed by any file under test automatically. 
#this file scope will un
#no need import them again there
from httpx import post
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from social_media_app.config import settings
from social_media_app.database import Base, get_db
from social_media_app.main import app
from social_media_app.oauth2 import create_access_token
from social_media_app import models
#from alembic import command

#Create a test database URL for SQLAlchemy to avoid overlap with DEV
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
#SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:Welcome1234@localhost/social_media_fastapi_test'

#Create a SQLAlchemy engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

#Create a SessionLocal class for testing other than Dev DB
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

@pytest.fixture
def session():
    #below statements are while using SQLalchemy
    #DROP Tables in Testing DB
    Base.metadata.drop_all(bind=engine)
    #create Tables in Testing DB
    Base.metadata.create_all(bind=engine)

    #alembic to create tables
    #command.upgrade("head")
    #command.downgrade("base")

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    #override the dependecies for testing
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "CARL1@gmail.com", "password": "PASSWORD"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "CARL2@gmail.com", "password": "PASSWORD"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers,
                      "Authorization": f'Bearer {token}'
                      }
    return client

@pytest.fixture
def test_posts(test_user,test_user2, session):
    posts_data = [{
        "title":"first title",
        "content": "first content",
        "owner_id" : test_user['id']
    }, 
    {
        "title":"Second title",
        "content": "Second content",
        "owner_id" : test_user['id']
    },
    {
        "title":"3rd title",
        "content": "3rd content",
        "owner_id" : test_user['id']
    },
    {
        "title":"4th title",
        "content": "4th content",
        "owner_id" : test_user['id']
    },
    {
        "title":"First post by second user title",
        "content": "First post by second user content",
        "owner_id" : test_user2['id']
    }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    '''session.add_all([models.Post(title = "first title", conent = "first content", owner_id = test_user['id']),
                     models.Post(title = "Second title", conent = "Second content", owner_id = test_user['id']),
                     models.Post(title = "3rd title", conent = "3rd content", owner_id = test_user['id']),
                     models.Post(title = "4th title", conent = "4th content", owner_id = test_user['id'])
                     ])'''
    session.commit()

    posts = session.query(models.Post).all()
    return posts