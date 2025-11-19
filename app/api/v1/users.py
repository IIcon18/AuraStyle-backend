from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.db import get_db
from app.services.auth_service import get_current_active_user_dependency
from app.models.user import User
from app.schemas.user import UserResponse
import os
import shutil
from fastapi.responses import FileResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def list_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user_dependency),
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_active_user_dependency),
):
    """Получить данные текущего аутентифицированного пользователя"""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user_dependency),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user_dependency),
):
    """Загрузить аватар пользователя"""

    # Проверяем что файл является изображением
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # Создаем папку для аватаров если её нет
    avatars_dir = "uploads/avatars"
    os.makedirs(avatars_dir, exist_ok=True)

    # Генерируем имя файла
    file_extension = file.filename.split('.')[-1]
    filename = f"avatar_{current_user.id}.{file_extension}"
    file_path = os.path.join(avatars_dir, filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Обновляем пользователя в БД
    current_user.avatar_url = f"/api/v1/users/me/avatar/{filename}"
    await db.commit()
    await db.refresh(current_user)

    return current_user


@router.get("/me/avatar/{filename}")
async def get_avatar(filename: str):
    """Получить аватар пользователя"""
    file_path = f"uploads/avatars/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )

    return FileResponse(file_path)