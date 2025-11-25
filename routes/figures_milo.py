from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app_core.database import SessionLocal
from app_core.models import Figure, Character
import json


router = APIRouter()

class FigureOut(BaseModel):
    figure_id: int
    character_id: int
    character_name: str
    rgb_color: str
    type: str

@router.get("/get_figures_milo/{milo_id}", response_model=List[FigureOut])
def get_figures_milo(milo_id: int):
    session: Session = SessionLocal()
    try:
        results = (
            session.query(Figure)
            .join(Character, Figure.character_id == Character.id)
            .filter(Figure.milo_id == milo_id)
            .all()
        )

        return [
            FigureOut(
                figure_id=f.id,
                character_id = f.character_id,
                character_name=f.character.name,
                rgb_color=f.character.rgb,
                type=f.type,
            )
            for f in results
        ]
    finally:
        session.close()
