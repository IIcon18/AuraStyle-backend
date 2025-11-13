# app/api/v1/auth.py
from fastapi import APIRouter, Depends
from app.services.auth_service import (
    AuthService,
    get_auth_service,
    get_current_active_user_dependency
)
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.authenticate_user(user_data)


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user_dependency)
):
    return current_user