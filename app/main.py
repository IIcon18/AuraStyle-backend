from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Aura Backend",
    version="1.0.0"
)

# Подключаем основной роутер
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Aura Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}