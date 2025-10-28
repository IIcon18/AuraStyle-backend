from fastapi import FastAPI
from app.core.db_init import init_database
from app.api.router import api_router

# Импортируем модели для регистрации в Base.metadata
from app.models.user import User
from app.models.session import Session
from app.models.image import Image
from app.models.result import Result

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_database()

app.include_router(api_router, prefix="/api/v1")