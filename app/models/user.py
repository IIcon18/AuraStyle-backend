from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(255), nullable=True)

    sessions = relationship("Session", back_populates="user")
    images = relationship("Image", back_populates="user")