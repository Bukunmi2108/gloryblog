from fastapi import APIRouter, Depends, HTTPException,FastAPI, Request, Response, status, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ..schema import *
from typing import *
from .. import models
from ..database import *
from .auth import get_current_user
from ..utils import get_password_hash
from datetime import datetime 


router = APIRouter(
    prefix="/user",
    tags=["User"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/loginform", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )

@router.post("/", status_code=201, response_model=UserResponse)
def create_user(request: Request, form: UserCreate = Form(...), db: Session = Depends(get_db)):
    try:
        form.password = get_password_hash(form.password)
        
        new_user = models.User(username=form.username, email=form.email, password=form.password)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{e}")
    return new_user


@router.get("/", response_model= List[UserResponse])
def get_user(response: Response, db: Session = Depends(get_db)):    
    users = db.query(models.User).all()
        
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Users Available")
    return users

@router.get("/profile")
async def get_user_profile_details(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
   
    user_id = current_user.id
    
    user_blogs = db.query(models.Blog).filter(models.Blog.author_id == user_id).all()

    user = db.query(models.User).filter(models.User.id == user_id).first()

    # Handle potential empty search results
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"User does not exist",
        )
    
    user_response = {
        "name": user.username,
        "email": user.email
    }

    user_blogs_details = [
        {
            "blog_id": blog.id,
            "blog_title": blog.title,
            "blog_content": blog.content,
            "blog_category": blog.category_name,
            "blog_created_at": blog.created_at,
            "author_id": blog.author_id,
            "author_name": user.username,
            "likes": blog.likes_count
        }
        for blog in user_blogs
    ]
    
    if user_blogs_details is None:
        user_blogs_details = 'You do not have any blogs created'

    return {
        "user": user_response,
        "blogs": user_blogs_details
    }


@router.get("/{id}", response_class=HTMLResponse)
def get_user_profile(request: Request, id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):    
    un_user = db.query(models.User).filter(models.User.id == id).first()
        
    if not un_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    user_blog = db.query(models.Blog).filter(models.Blog.author_id == id).all()
    
    context = {
        "user": un_user,
        "blogs": user_blog
    }
    
    return context
