from fastapi import APIRouter, Depends, HTTPException,FastAPI, Request, Form, Body, status, Query
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload
from ..schema import BlogResponse, Category, BlogCreate, CategoryCreate, Tag, CategoryResponse, AuthorResponse, BlogWithUsername, SearchQuery, CategoryName
from typing import *
from .. import models
from ..database import *
from .auth import get_current_user
from sqlalchemy import or_, func


router = APIRouter(
    prefix="/blog",
    tags=["Blog"],
)


@router.get("/all")
def get_blogs(request: Request, db: Session = Depends(get_db)):
    
    blogs_with_user = db.query(models.Blog, models.User).join(models.User, models.Blog.author_id == models.User.id).all()
    
    blogs_with_user_details = [
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
        for blog, user in blogs_with_user
    ]

    return blogs_with_user_details

@router.get("/search")
async def search_blogs(query: SearchQuery = Query(...), db: Session = Depends(get_db)):
   
    search_terms = query.q
    blogs_with_user = db.query(models.Blog, models.User).join(models.User, models.Blog.author_id == models.User.id).filter(models.Blog.title.contains(search_terms) | models.Blog.content.contains(search_terms)).all()

    # Handle potential empty search results
    if not len(blogs_with_user):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=F"No blogs found for '{query.q}'",
        )

    blogs_with_user_details = [
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
        for blog, user in blogs_with_user
    ]

    return blogs_with_user_details


def get_like(user_id: int, blog_id: int, db: Session = Depends(get_db)):
    return db.query(models.Like).filter(models.Like.user_id == user_id, models.Like.blog_id == blog_id).first()


@router.get("/tags", response_model=List[Tag])
def get_blogs(request: Request, db: Session = Depends(get_db)):
    
    tags = db.query(models.Tag).all()
    
    return tags

@router.get("/tag/{id}")
async def get_blogs_with_tags(id: int, db: Session = Depends(get_db)):
       
    category = db.query(models.Category).filter(models.Category.tag_id == id).all()
    
    if not category:
        return {"error": "Category not found"}
    return category

@router.get("/category/get")
async def get_blogs_with_category(category_name: CategoryName = Query(...), db: Session = Depends(get_db)):
   
    blogs_with_user = db.query(models.Blog, models.User).join(models.User, models.Blog.author_id == models.User.id).filter(models.Blog.category_name == category_name.q).all()

    # Handle potential empty search results
    if not len(blogs_with_user):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=F"No blogs found for '{category_name}'",
        )

    blogs_with_user_details = [
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
        for blog, user in blogs_with_user
    ]

    return blogs_with_user_details


@router.get("/category", response_model=List[Category])
def get_blogs(request: Request, db: Session = Depends(get_db)):
    
    categories = db.query(models.Category).order_by(models.Category.name).all()
    # print(categories)
    return categories

@router.post("/category", status_code=status.HTTP_201_CREATED)
def create_blog(category: CategoryCreate = Body(...), current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    
    category_name = category.name
    category_tag = category.tag_id
    
    check = db.query(models.Category).filter(models.Category.name == category_name).first()
    
    if check is None:
        newcategory = models.Category(name=category_name, tag_id= category_tag)
        
        db.add(newcategory)
        db.commit()
        db.refresh(newcategory)

        return newcategory
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name already in use")


@router.get("/{blog_id}", response_model=BlogResponse)
def read_blog(request: Request, blog_id: int, db: Session = Depends(get_db)):
    
    blog_with_user = db.query(models.Blog).join(models.User, models.Blog.author_id == models.User.id).filter(models.Blog.id == blog_id).first()
        
    if not blog_with_user:
        raise HTTPException(status_code=404, detail="Blog not found")

    author_name = blog_with_user.author.username  # Access the author name using the backref
    
    response_model = BlogResponse(
        id= blog_with_user.id,
        title= blog_with_user.title,
        content= blog_with_user.content,
        category_name= blog_with_user.category_name,
        created_at= blog_with_user.created_at,
        author_id= blog_with_user.author_id,
        likes=blog_with_user.likes_count,
        author_name= BlogWithUsername(name=author_name)
    )
    return response_model

    
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate = Body(...), current_user = Depends(get_current_user),  db: Session = Depends(get_db)):
    
    title = blog.title
    content = blog.content
    category_name = blog.category_name

    newblog = models.Blog(title=title, content=content, category_name=category_name, author_id=current_user.id)
    
    db.add(newblog)
    db.commit()
    db.refresh(newblog)

    return newblog


@router.post("/{blog_id}/likes", status_code=status.HTTP_201_CREATED)
def like_post(blog_id: int, current_user = Depends(get_current_user),  db: Session = Depends(get_db)):
    # Check if the user has already liked the post
    existing_like = db.query(models.Like).filter(models.Like.user_id == current_user.id, models.Like.blog_id == blog_id).first()
    
    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked this post.")

    # Create a new like
    like = models.Like(user_id=current_user.id, blog_id=blog_id)
    db.add(like)
    
    # Update the likes count
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    blog.likes_count += 1
    
    db.commit()
    db.refresh(like)

    return like

@router.delete("/{blog_id}/likes", status_code=204)
def unlike_post(blog_id: int, current_user = Depends(get_current_user),  db: Session = Depends(get_db)):
    # Check if the user has liked the post
    existing_like = db.query(models.Like).filter(models.Like.user_id == current_user.id, models.Like.blog_id == blog_id).first()
    
    if not existing_like:
        raise HTTPException(status_code=404, detail="You have not liked this post.")

    # Delete the like
    db.delete(existing_like)
    
    # Update the likes count
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    blog.likes_count -= 1
    
    db.commit()

    return None