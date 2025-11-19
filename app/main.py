from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.router import api_router
from app.core.db_init import init_database
from app.core.db import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select, text

app = FastAPI(title="AuraStyle API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # Проверяем флаг RESET_DATABASE
    reset_db = os.getenv("RESET_DATABASE", "false").lower() == "true"

    if reset_db:
        print("🔄 Пересоздание БД...")
        # Удаляем и пересоздаем таблицы
        async with AsyncSessionLocal() as session:
            try:
                # Удаляем все таблицы
                await session.execute(text("DROP TABLE IF EXISTS results CASCADE"))
                await session.execute(text("DROP TABLE IF EXISTS images CASCADE"))
                await session.execute(text("DROP TABLE IF EXISTS sessions CASCADE"))
                await session.execute(text("DROP TABLE IF EXISTS users CASCADE"))
                await session.commit()
                print("✅ Старые таблицы удалены")
            except Exception as e:
                print(f"⚠️ Ошибка при удалении таблиц: {e}")
                await session.rollback()

    await init_database()
    print("✅ AuraStyle backend запущен!")

    # Проверка что БД работает
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"✅ База данных подключена. Пользователей в БД: {len(users)}")

@app.get("/")
async def root():
    base_url = "http://localhost:8000"

    return {
        "app": "AuraStyle",
        "message": "AI-powered style analysis platform",
        "links": {
            "🔐 Auth": f"{base_url}/api/v1/auth",
            "👤 Users": f"{base_url}/api/v1/users",
            "🖼️ Analysis": f"{base_url}/api/v1/analysis",
            "📚 API Docs": f"{base_url}/docs",
            "📖 ReDoc": f"{base_url}/redoc"
        }
    }