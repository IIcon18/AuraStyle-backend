from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.db_init import init_database  # если у тебя есть init_database
from app.core.db import AsyncSessionLocal    # твоя сессия БД
from app.models.user import User            # твоя модель User
from sqlalchemy import select

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

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    await init_database()  # если у тебя есть инициализация БД
    print("✅ AuraStyle backend запущен!")

    # Опционально: проверка что БД работает
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