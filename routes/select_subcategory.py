from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import StorySubcategory, Milo


router = APIRouter()


class SelectSubcategoryRequest(BaseModel):
    story_subcategory_id: int


@router.post("/select_subcategory/{milo_id}")
def select_subcategory(milo_id: int, payload: SelectSubcategoryRequest):
    session: Session = SessionLocal()
    try:
        subcategory = (
            session.query(StorySubcategory)
            .filter(StorySubcategory.id == payload.story_subcategory_id)
            .first()
        )

        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")

        milo = session.query(Milo).filter(Milo.id == milo_id).first()
        if not milo:
            raise HTTPException(status_code=404, detail="Milo not found")

        milo.story_subcategories_id = subcategory.id
        session.commit()

        return {
            "milo_id": milo.id,
            "story_subcategory_id": subcategory.id,
        }
    finally:
        session.close()