from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import StoryCategory, StorySubcategory


router = APIRouter()


class StorySubcategoryOut(BaseModel):
    id: int
    name: str


class GetSubcategoriesResponse(BaseModel):
    story_category_description: Optional[str]
    subcategories: List[StorySubcategoryOut]


@router.get("/get_subcategories/{story_category_id}", response_model=GetSubcategoriesResponse)
def get_subcategories(story_category_id: int):
    session: Session = SessionLocal()
    try:
        category = (
            session.query(StoryCategory)
            .filter(StoryCategory.id == story_category_id)
            .first()
        )

        if not category:
            raise HTTPException(status_code=404, detail="Story category not found")

        return GetSubcategoriesResponse(
            story_category_description=category.description,
            subcategories=[
                StorySubcategoryOut(id=sub.id, name=sub.name)
                for sub in category.subcategories
            ],
        )
    finally:
        session.close()