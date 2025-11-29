from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import Milo

router = APIRouter()


class Credits(BaseModel):
    credit: int

@router.get("/get_credits/{milo_id}", response_model=Credits)
def get_credits(milo_id: int):
    session: Session = SessionLocal()
    try:
        milo = session.query(Milo).filter(Milo.id == milo_id).first()
        
        return Credits(credit = milo.credits)
        
    finally:
        session.close()
