from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister

# Простая Bearer аутентификация
security = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> Optional[User]:
    try:
        user_result = await db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            print(f"❌ Пользователь с email {login_data.email} не найден")
            return None

        if not verify_password(login_data.password, user.password_hash):
            print("❌ Неверный пароль")
            return None

        print(f"✅ Пользователь {user.email} аутентифицирован")
        return user
    except Exception as e:
        print(f"❌ Ошибка аутентификации: {e}")
        return None

async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
    try:
        print(f"🔵 Начало регистрации пользователя: {user_data.email}")

        # Проверяем email
        existing_user = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

        # Проверяем username
        existing_username = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        if existing_username.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

        # Хешируем пароль
        hashed_password = hash_password(user_data.password)
        print("🔵 Пароль захэширован")

        # Создаем пользователя
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        print(f"✅ Пользователь {new_user.email} создан с ID {new_user.id}")
        return new_user

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Критическая ошибка регистрации: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Вспомогательная функция для получения пользователя по токену
async def get_current_user(db: AsyncSession, token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        print(f"🔵 Декодирован токен для user_id: {user_id}")
    except JWTError as e:
        print(f"❌ Ошибка JWT: {e}")
        raise credentials_exception

    user_result = await db.execute(select(User).where(User.id == int(user_id)))
    user = user_result.scalar_one_or_none()
    if user is None:
        print(f"❌ Пользователь с ID {user_id} не найден в БД")
        raise credentials_exception

    print(f"✅ Найден пользователь: {user.email}")
    return user

# Зависимости для защиты эндпоинтов
async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await get_current_user(db, credentials.credentials)

async def get_current_active_user_dependency(
    current_user: User = Depends(get_current_user_dependency)
) -> User:
    return current_user