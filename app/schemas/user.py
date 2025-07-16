from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    photo: Optional[str] = None
    video: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
    profile: Optional[Profile] = None

    class Config:
        orm_mode = True
