from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from typing import Optional
from app.sсhemas.user import UserResponse
from app.sсhemas.analysis import StyleAnalysisResponse

router = APIRouter()

# Временные данные
fake_users = [
    {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "avatar_url": None,
        "is_active": True
    }
]

fake_analysis_history = [
    {
        "id": 1,
        "user_id": 1,
        "image_url": "/uploads/photo1.jpg",
        "style_type": "casual",
        "dominant_colors": ["blue", "white", "black"],
        "style_score": 75.5,
        "created_at": "2023-12-01T10:00:00"
    },
    {
        "id": 2,
        "user_id": 1,
        "image_url": "/uploads/photo2.jpg",
        "style_type": "sport",
        "dominant_colors": ["red", "black", "white"],
        "style_score": 88.0,
        "created_at": "2023-12-02T11:00:00"
    }
]


def get_current_user(authorization: Optional[str] = Header(None)):
    """Временная функция для получения текущего пользователя"""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    # Временная логика - всегда возвращаем тестового пользователя
    return fake_users[0]


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return user


@router.put("/avatar")
async def update_avatar(file: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Сохраняем информацию о файле (временная реализация)
    avatar_url = f"/avatars/{file.filename}"

    return {
        "message": "Avatar updated successfully",
        "filename": file.filename,
        "avatar_url": avatar_url
    }


@router.get("/history")
async def get_analysis_history(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Возвращаем историю анализов для текущего пользователя
    user_history = [item for item in fake_analysis_history if item["user_id"] == user["id"]]

    return {
        "user_id": user["id"],
        "history": user_history,
        "total": len(user_history)
    }