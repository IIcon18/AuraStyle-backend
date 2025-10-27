from fastapi import APIRouter, HTTPException, status
from app.sсhemas.user import UserCreate, UserLogin, Token, UserResponse

router = APIRouter()

# Временное хранилище пользователей (заменится на БД)
fake_users_db = []


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    # Проверяем, нет ли уже такого пользователя
    for user in fake_users_db:
        if user["email"] == user_data.email or user["username"] == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already exists"
            )

    # Создаем нового пользователя
    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user_data.username,
        "email": user_data.email,
        "avatar_url": None,
        "is_active": True
    }
    fake_users_db.append(new_user)

    return new_user


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    # Ищем пользователя по email или username
    user = None
    for u in fake_users_db:
        if u["email"] == login_data.login or u["username"] == login_data.login:
            user = u
            break

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )

    # Временный токен (заменится на JWT)
    return {
        "access_token": f"fake-jwt-token-for-user-{user['id']}",
        "token_type": "bearer"
    }