from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import StorySubcategory


router = APIRouter()


class StorySubcategoryOut(BaseModel):
    id: int
    name: str


@router.get("/get_subcategories/{story_category_id}", response_model=List[StorySubcategoryOut])
def get_subcategories(story_category_id: int):
    session: Session = SessionLocal()
    try:
        subcategories = (
            session.query(StorySubcategory)
            .filter(StorySubcategory.story_categories_id == story_category_id)
            .all()
        )

        return [
            StorySubcategoryOut(
                id=sub.id,
                name=sub.name,
            )
            for sub in subcategories
        ]
    finally:
        session.close()