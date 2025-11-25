from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app_core.database import SessionLocal
from app_core.models import Figure, Character


router = APIRouter()

class FigureInfoOut(BaseModel):
    figure_id: int
    character_id: int
    character_name: str
    background: str
    custom_properties: str

@router.get("/get_figure_infos/{figure_id}", response_model=FigureInfoOut)
def get_figure_infos(figure_id: int):
    session: Session = SessionLocal()
    try:
        figure = (
            session.query(Figure)
            .join(Character, Figure.character_id == Character.id)
            .filter(Figure.id == figure_id)
            .first()
        )

        if not figure:
            raise HTTPException(status_code=404, detail="Figure not found")

        return FigureInfoOut(
            figure_id=figure.id,
            character_name=figure.character.name,
            character_id = figure.character_id,
            background=figure.character.background,
            custom_properties=figure.custom_properties,
        )
    finally:
        session.close()
