from enum import IntEnum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.networks import EmailStr
from app.database import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class VoteEnum(IntEnum):
    like = 1
    unlike = 0


class Vote(BaseModel):
    post_id: int
    dir: VoteEnum


class PostOut(BaseModel):
    Post: Post
    votes: int
