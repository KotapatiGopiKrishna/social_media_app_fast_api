from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from fastapi.params import Body

from . import models
from .database import engine
from .routers import post,user, auth, vote
from .config import settings

# this will create a tables as mentioned in the models.py file
# since alembic is enable below command is no longer needed
#models.Base.metadata.create_all(bind=engine)

#create a new instance
app = FastAPI()

#domains can be allowed through middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#link the routes from router folder files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {"message" : "Hello world"}