from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app_core.database import SessionLocal
from app_core.models import Figure
from typing import List

router = APIRouter()

class FigureInfoOut(BaseModel):
    figure_id: int
    character_id: int
    character_name: str
    background: str
    character_properties: List[str]
    custom_properties: int

class CustomPropertiesUpdate(BaseModel):
    value: int
    
@router.post("/update_custom_properties/{figure_id}", response_model=FigureInfoOut)
def figures_infos_modif_customproperties(figure_id: int, data: CustomPropertiesUpdate):
    session: Session = SessionLocal()
    try:
        figure = session.query(Figure).filter(Figure.id == figure_id).first()

        if not figure:
            raise HTTPException(status_code=404, detail="Figure not found")
        
        print(f"Updating figure {figure_id} with value {data.value}")  # log

        figure.custom_properties = data.value

        session.commit()
        session.refresh(figure)

        return FigureInfoOut(
            figure_id=figure.id,
            character_id=figure.character_id,
            character_name=figure.character.name,
            background=figure.character.background,
            character_properties=figure.character.properties or [],
            custom_properties=figure.custom_properties
        )

    finally:
        session.close()