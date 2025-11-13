from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime

class AnalysisResponse(BaseModel):
    image_id: int
    result_id: int
    analysis: Dict[str, Any]
    analyzed_at: datetime

class AnalysisResult(BaseModel):
    style: str
    confidence: float
    colors: List[str]
    recommendations: List[str]