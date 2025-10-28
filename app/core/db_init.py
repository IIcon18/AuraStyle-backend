from app.core.db import engine, Base
from app.core.config import settings


async def init_database():
    """Инициализация базы данных - создание всех таблиц"""
    async with engine.begin() as conn:
        if settings.RESET_DATABASE:
            print("🔄 RESET_DATABASE=true - Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            print("✅ All tables dropped")

        print("🔄 Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ All tables created successfully")