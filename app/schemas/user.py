from pydantic import BaseModel, field_validator
from typing import Optional
import re


class UserBase(BaseModel):
    username: str
    email: str

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    login: str  # email или username
    password: str


class UserResponse(UserBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None