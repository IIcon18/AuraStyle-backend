from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserResponse  # ← импортируем напрямую

router = APIRouter()


@router.post("/login", response_model=UserResponse)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # Ищем пользователя по email или username
    result = await db.execute(
        select(User).where(
            (User.email == login_data.login) | (User.username == login_data.login)
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Временная проверка пароля
    if user.password_hash != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    return user


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user