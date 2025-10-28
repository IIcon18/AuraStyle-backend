from pydantic import BaseModel
from app.schemas.image import ImageResponse
from app.schemas.result import ResultResponse

class AnalysisResponse(BaseModel):
    image: ImageResponse
    result: ResultResponse