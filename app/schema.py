from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlogWithUsername(BaseModel):
    name: str
    
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    category_name: str
    created_at: datetime
    author_id: int
    author_name: BlogWithUsername
    likes: int
    
class BlogCreate(BaseModel):
    title: str
    content: str
    category_name: str

class Tag(BaseModel):
    id: int
    name: str

class Category(BaseModel):
    id: int
    name: str
    tag_id: int

class CategoryResponse(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    name: str
    tag_id: int

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

#User Registration
class UserResponse(BaseModel):
    email: str
    id: int
    # created_at: datetime
    
class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

#Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: Optional[int] = None

class AuthorResponse(BaseModel):
    username: str
    
# class Config:
#     orm_mode = True

class SearchQuery(BaseModel):
    q: str
class CategoryName(BaseModel):
    q: str