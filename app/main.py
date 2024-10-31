from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import *
from .router import blog, user, auth
from dotenv import load_dotenv

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(blog.router)
app.include_router(auth.router)


@app.get("/")
def read_index(request: Request):
    return {'message': 'Welcome to Glory Blog'}
