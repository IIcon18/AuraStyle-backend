from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str]
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str