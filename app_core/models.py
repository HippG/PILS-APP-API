from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app_core.database import Base

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    voice_id = Column(String)
    background = Column(String)
    rgb = Column(String)

class Figure(Base):
    __tablename__ = "figures"
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    release_date = Column(String)
    custom_properties = Column(String)
    type = Column(String)
    environment_id = Column(Integer)
    rfid_uid = Column(String)
    milo_id = Column(Integer)
    character = relationship("Character")
