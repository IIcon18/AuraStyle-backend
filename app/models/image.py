from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import BaseModel


class Image(BaseModel):
    __tablename__ = "images"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_path = Column(String(255), nullable=False)

    user = relationship("User", back_populates="images")
    result = relationship("Result", back_populates="image", uselist=False)