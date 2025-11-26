from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import StoryCategory


router = APIRouter()


class StoryCategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]


@router.get("/get_categories", response_model=List[StoryCategoryOut])
def get_categories():
    session: Session = SessionLocal()
    try:
        categories = session.query(StoryCategory).all()

        return [
            StoryCategoryOut(
                id=category.id,
                name=category.name,
                description=category.description,
            )
            for category in categories
        ]
    finally:
        session.close()