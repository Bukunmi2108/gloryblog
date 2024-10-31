from fastapi import APIRouter, Depends, HTTPException,FastAPI, Request, Response, status, Form
import requests
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schema import *
from typing import *
from .. import models
from ..database import *
from ..utils import verify_password
from datetime import datetime 
from ..config import settings


router = APIRouter(
    tags=["Login"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
        
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login(request:Request, response:Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid  Credentials")
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials password")
    
    access_token = create_access_token({"sub": user.id})
    response.set_cookie(key="accessToken", value=access_token)
        
    return {"access_token": access_token, "token_type": "bearer"}


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ID not found")
        token_data = TokenData(id=id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")
    
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token["sub"]).first()
    
    return user


# @router.post("/req/{URL}")
# async def send_request(URL: str, request: Request, token: str = Depends(oauth2_scheme)):
#     url = URL
    
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
    
#     response = requests.get(url, headers=headers)

#     return response
