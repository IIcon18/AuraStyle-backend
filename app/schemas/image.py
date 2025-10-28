from pydantic import BaseModel
from datetime import datetime


class ImageResponse(BaseModel):
    id: int
    user_id: int
    image_path: str
    created_at: datetime

    class Config:
        from_attributes = True