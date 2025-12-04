from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app_core.database import Base

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    voice_id = Column(String)
    background = Column(String)
    rgb = Column(String)
    rgb_app = Column(String)
    properties = Column(ARRAY(String))

class Figure(Base):
    __tablename__ = "figures"
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    release_date = Column(String)
    custom_properties = Column(Integer)
    type = Column(String)
    environment_id = Column(Integer)
    rfid_uid = Column(String)
    milo_id = Column(Integer)
    character = relationship("Character")
    
class StoryCategory(Base):
    __tablename__ = "story_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    subcategories = relationship("StorySubcategory", back_populates="category")


class StorySubcategory(Base):
    __tablename__ = "story_subcategories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    story_categories_id = Column(Integer, ForeignKey("story_categories.id"))
    category = relationship("StoryCategory", back_populates="subcategories")
    milos = relationship("Milo", back_populates="subcategory")  # ✅ nouveau lien vers Milo

class SavedStory(Base):
    __tablename__ = "saved_stories"

    id = Column(Integer, primary_key=True)
    milo_id = Column(Integer, ForeignKey("milo.id"))

    s3_key = Column(String)
    length = Column(Integer)
    created_at = Column(String)
    title = Column(String)
    milo = relationship("Milo", back_populates="stories")


class Milo(Base):
    __tablename__ = "milo"
    id = Column(Integer, primary_key=True)
    credits = Column(Integer)
    story_subcategories_id = Column(Integer, ForeignKey("story_subcategories.id"))  # ✅ nouveau FK
    subcategory = relationship("StorySubcategory", back_populates="milos")
    stories = relationship("SavedStory", back_populates="milo")
