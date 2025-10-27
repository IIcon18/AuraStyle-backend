from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StyleAnalysisResponse(BaseModel):
    id: int
    user_id: int
    image_url: str
    style_type: Optional[str] = None
    dominant_colors: Optional[List[str]] = None
    style_score: Optional[float] = None
    created_at: datetime