from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, TIMESTAMP, text, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # Relationship with BlogPost (one-to-many)
    posts = relationship("Blog", backref="author", cascade="all, delete-orphan")
    
    likes = relationship("Like", backref="user")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String(255), nullable=False)
    content = Column(UnicodeText, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


    # Foreign key relationship with User (many-to-one)
    author_id = Column(Integer, ForeignKey("users.id"))
    category_name = Column(String, ForeignKey("categories.name"), nullable=False)
    
    likes = relationship("Like", backref="post")
    likes_count = Column(Integer, default=0)


class Category(Base):
    __tablename__ = "categories"
    
    name = Column(String, nullable=False, unique=True)
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)
    
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    
