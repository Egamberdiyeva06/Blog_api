from pydantic import BaseModel, Field
from typing import List, Optional


class PostBase(BaseModel):
    title: str = Field(max_length=100)
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None


class PostOut(PostBase):
    id: int
    user_id: int
    likes_count: int = 0
    comments_count: int = 0

    class Config:
        from_attributes = True



class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    posts: List[PostOut] = []
    comments: List[CommentOut] = []
    liked_posts: List[PostOut] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str



class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    post_id: int


class CommentOut(CommentBase):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True



class LikeOut(BaseModel):
    user_id: int
    post_id: int
