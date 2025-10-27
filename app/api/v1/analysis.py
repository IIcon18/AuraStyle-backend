from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from typing import List, Optional
from app.sсhemas.analysis import StyleAnalysisResponse
from datetime import datetime

router = APIRouter()

# Временное хранилище анализов
fake_analyses = [
    {
        "id": 1,
        "user_id": 1,
        "image_url": "/uploads/photo1.jpg",
        "style_type": "casual",
        "dominant_colors": ["blue", "white", "black"],
        "style_score": 75.5,
        "created_at": "2023-12-01T10:00:00"
    }
]


def get_current_user_id(authorization: Optional[str] = Header(None)):
    """Временная функция для получения ID текущего пользователя"""
    # Всегда возвращаем ID 1 для тестирования
    return 1


@router.post("/analyze", response_model=StyleAnalysisResponse)
async def analyze_style(file: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)

    # Проверяем тип файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    # Временная логика анализа (заменится на ML модель)
    new_analysis = {
        "id": len(fake_analyses) + 1,
        "user_id": user_id,
        "image_url": f"/uploads/{file.filename}",
        "style_type": "casual",  # временный результат
        "dominant_colors": ["blue", "white", "black"],  # временный результат
        "style_score": 82.5,  # временный результат
        "created_at": datetime.now().isoformat()
    }

    fake_analyses.append(new_analysis)

    return new_analysis


@router.get("/history", response_model=List[StyleAnalysisResponse])
async def get_user_analysis_history(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)

    # Возвращаем анализы только для текущего пользователя
    user_analyses = [analysis for analysis in fake_analyses if analysis["user_id"] == user_id]

    return user_analyses


@router.delete("/reset")
async def reset_analysis(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)

    # Удаляем анализы текущего пользователя
    global fake_analyses
    fake_analyses = [analysis for analysis in fake_analyses if analysis["user_id"] != user_id]

    return {
        "message": "Analysis history cleared successfully",
        "deleted_user_id": user_id
    }