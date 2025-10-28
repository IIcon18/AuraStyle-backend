from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.base import BaseModel


class Result(BaseModel):
    __tablename__ = "results"

    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    style_type = Column(String(100))  # спортивный, кэжуал и тд
    confidence_score = Column(Float)  # уровень уверенности 0-100
    dominant_colors = Column(String(255))  # JSON как строка

    image = relationship("Image", back_populates="result")