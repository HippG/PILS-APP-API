from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import Milo

router = APIRouter()


class SelectedSubcategoryOut(BaseModel):
    id: int
    name: str


class LinkedCategoryOut(BaseModel):
    id: int
    name: str


class GetSelectedResponse(BaseModel):
    selected_subcategory: SelectedSubcategoryOut
    linked_category: LinkedCategoryOut


@router.get("/get_selected/{milo_id}", response_model=GetSelectedResponse)
def get_selected(milo_id: int):
    session: Session = SessionLocal()
    try:
        milo = session.query(Milo).filter(Milo.id == milo_id).first()

        if not milo:
            raise HTTPException(status_code=404, detail="Milo not found")

        subcategory = milo.subcategory
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not selected for this Milo")

        category = subcategory.category
        if not category:
            raise HTTPException(status_code=404, detail="Category not linked to selected subcategory")

        return GetSelectedResponse(
            selected_subcategory=SelectedSubcategoryOut(id=subcategory.id, name=subcategory.name),
            linked_category=LinkedCategoryOut(id=category.id, name=category.name),
        )
    finally:
        session.close()
