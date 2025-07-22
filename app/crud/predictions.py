from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.models import Prediction
from app.schemas.prediction import PredictionCreate
from typing import List, Optional
import uuid

class PredictionCRUD:
    async def create_prediction(
        self, 
        db: AsyncSession, 
        prediction_data: PredictionCreate,
        user_id: uuid.UUID
    ) -> Prediction:
        db_prediction = Prediction(
            user_id=user_id,
            request_id=str(uuid.uuid4()),
            **prediction_data.dict()
        )
        db.add(db_prediction)
        await db.commit()
        await db.refresh(db_prediction)
        return db_prediction
    
    async def get_user_predictions(
        self, 
        db: AsyncSession, 
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Prediction]:
        query = (
            select(Prediction)
            .where(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

prediction_crud = PredictionCRUD()
