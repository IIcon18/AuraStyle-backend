from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.image import Image
from app.models.result import Result
from app.schemas.analysis import AnalysisResponse  # ← импортируем напрямую
import aiofiles
import os
import uuid
import json

router = APIRouter()

# Константы для загрузки файлов
UPLOAD_DIR = "uploads"
IMAGE_DIR = "uploads/images"


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_style(
        file: UploadFile = File(...),
        user_id: int = 1,
        db: AsyncSession = Depends(get_db)
):
    # Проверяем тип файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Сохраняем файл с уникальным именем
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"{IMAGE_DIR}/{unique_filename}"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Создаем запись в images
    image = Image(
        user_id=user_id,
        image_path=file_path
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)

    # Создаем результат анализа (заглушка для ML)
    result = Result(
        image_id=image.id,
        style_type="casual",
        confidence_score=82.5,
        dominant_colors=json.dumps(["blue", "white", "black"])
    )

    db.add(result)
    await db.commit()
    await db.refresh(result)

    return {
        "image": image,
        "result": result
    }


@router.get("/history/{user_id}")
async def get_analysis_history(user_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем все анализы пользователя с join images и results
    result = await db.execute(
        select(Image, Result)
        .join(Result, Image.id == Result.image_id)
        .where(Image.user_id == user_id)
        .order_by(Image.created_at.desc())
    )
    analyses = result.all()

    return {
        "user_id": user_id,
        "history": [
            {
                "analysis_id": result.id,
                "image_id": image.id,
                "image_path": image.image_path,
                "style_type": result.style_type,
                "confidence_score": result.confidence_score,
                "dominant_colors": json.loads(result.dominant_colors) if result.dominant_colors else [],
                "analyzed_at": result.created_at
            }
            for image, result in analyses
        ]
    }


@router.delete("/reset/{user_id}")
async def reset_analysis(user_id: int, db: AsyncSession = Depends(get_db)):
    # Находим все изображения пользователя
    result = await db.execute(
        select(Image).where(Image.user_id == user_id)
    )
    user_images = result.scalars().all()

    # Удаляем результаты и изображения
    for image in user_images:
        await db.execute(
            Result.__table__.delete().where(Result.image_id == image.id)
        )
        await db.execute(
            Image.__table__.delete().where(Image.id == image.id)
        )

    await db.commit()

    return {"message": f"Analysis history cleared for user {user_id}"}