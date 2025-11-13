from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.auth_service import get_current_active_user_dependency
from app.models.user import User
from app.models.image import Image
from app.models.result import Result
from app.schemas.analysis import AnalysisResponse
from datetime import datetime

router = APIRouter()


@router.post("/analyze-image", response_model=AnalysisResponse)
async def analyze_image(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user_dependency),
):
    # Проверяем тип файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # Читаем файл
    contents = await file.read()

    # Сохраняем информацию об изображении в БД
    image = Image(
        user_id=current_user.id,
        filename=file.filename,
        content_type=file.content_type,
        file_size=len(contents),
        # Здесь можно сохранить файл в хранилище или обработать его
    )

    db.add(image)
    await db.commit()
    await db.refresh(image)

    # Здесь будет логика анализа изображения ML моделью
    # Пока заглушка
    analysis_result = {
        "style": "casual",
        "confidence": 0.85,
        "colors": ["blue", "white", "black"],
        "recommendations": ["Great for everyday wear", "Matches your skin tone well"]
    }

    # Сохраняем результат анализа
    result = Result(
        image_id=image.id,
        user_id=current_user.id,
        analysis_data=analysis_result
    )

    db.add(result)
    await db.commit()
    await db.refresh(result)

    return AnalysisResponse(
        image_id=image.id,
        result_id=result.id,
        analysis=analysis_result,
        analyzed_at=datetime.utcnow()
    )


@router.get("/results")
async def get_analysis_results(
        skip: int = 0,
        limit: int = 20,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user_dependency),
):
    # Получаем результаты анализа для текущего пользователя
    from sqlalchemy import select
    from app.models.result import Result
    from app.models.image import Image

    stmt = select(Result).join(Image).where(Result.user_id == current_user.id)
    stmt = stmt.offset(skip).limit(limit).order_by(Result.created_at.desc())

    result = await db.execute(stmt)
    results = result.scalars().all()

    return results