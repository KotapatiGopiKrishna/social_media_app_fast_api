
from jose import jwt
import pytest
from social_media_app import schemas
from social_media_app.config import settings

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello world'

def test_create_user(client):
    res = client.post("/users/", json={"email": "CARL1@gmail.com", "password": "PASSWORD"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "CARL1@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert login_res.token_type == "bearer"
    assert id == test_user['id']
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
                         ("CARL1@gmail.com","wrongpassword",403),
                         ("CARL123@gmail.com","PASSWORD",403),
                         (None,"PASSWORD",422),
                         ("CARL123@gmail.com",None,422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    
    if res.status_code != 422:
        assert res.json().get('detail') == 'Invalid Credentials'