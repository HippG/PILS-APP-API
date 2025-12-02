import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError

from app_core.database import SessionLocal
from app_core.models import SavedStory  # <-- IMPORTANT : on utilise saved_stories


# -------------------------------------------------
# ROUTER
# -------------------------------------------------

router = APIRouter(tags=["story"])


# -------------------------------------------------
# AWS S3 CONFIG
# -------------------------------------------------

AWS_REGION = "eu-west-3"
BUCKET_NAME = "milo-amzn-s3-stories"
PRESIGNED_EXPIRATION = 3600

s3_client = boto3.client("s3", region_name=AWS_REGION)


# -------------------------------------------------
# RESPONSE MODELS
# -------------------------------------------------

class StoryInfo(BaseModel):
    id: int
    length: int
    created_at: str

class StoryIdRequest(BaseModel):
    id: int


# -------------------------------------------------
# ENDPOINT 1 : LISTE DES STORIES POUR UN MILO
# -------------------------------------------------

@router.get("/get_story/{milo_id}", response_model=list[StoryInfo])
def get_stories(milo_id: int):
    session: Session = SessionLocal()
    try:
        stories = (
            session.query(SavedStory)
            .filter(SavedStory.milo_id == milo_id)
            .all()
        )

        if not stories:
            raise HTTPException(status_code=404, detail="Aucune story trouvée pour ce Milo")

        return [
            StoryInfo(
                id=s.id,
                length=s.length,
                created_at=str(s.created_at)
            )
            for s in stories
        ]

    finally:
        session.close()


# -------------------------------------------------
# ENDPOINT 2 : PRESIGNED URL POUR UNE STORY
# -------------------------------------------------

@router.post("/get_story/presign")
def presign_story(request: StoryIdRequest):
    session: Session = SessionLocal()
    try:
        story = session.query(SavedStory).filter(SavedStory.id == request.id).first()

        if not story:
            raise HTTPException(status_code=404, detail="Story not found")

        if not story.s3_key:
            raise HTTPException(status_code=400, detail="Cette story n’a pas de s3_key associé")

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_NAME, "Key": story.s3_key},
                ExpiresIn=PRESIGNED_EXPIRATION
            )
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Erreur AWS : {e}")

        return {
            "story_id": story.id,
            "s3_key": story.s3_key,
            "presigned_url": url
        }

    finally:
        session.close()
