from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_core.database import SessionLocal
from app_core.models import Milo

router = APIRouter()


class MiloExistsResponse(BaseModel):
    exists: bool


@router.get("/milo_exists/{milo_id}", response_model=MiloExistsResponse)
def milo_exists(milo_id: int):
    session: Session = SessionLocal()
    try:
        exists = session.query(Milo).filter(Milo.id == milo_id).first() is not None
        return MiloExistsResponse(exists=exists)
    finally:
        session.close()
