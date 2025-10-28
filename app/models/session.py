from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import BaseModel


class Session(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")