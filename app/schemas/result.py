from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ResultBase(BaseModel):
    style_type: Optional[str] = None
    confidence_score: Optional[float] = None
    dominant_colors: Optional[List[str]] = None


class ResultResponse(ResultBase):
    id: int
    image_id: int
    created_at: datetime

    class Config:
        from_attributes = True