from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models import TopicProgress
from app.models.user import User
from app.schemas import ProgressOut

router = APIRouter()

@router.get("/progress", response_model=list[ProgressOut])
def list_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    uid = str(current_user.id)
    rows = db.query(TopicProgress).filter(TopicProgress.user_id == uid).all()
    return [
        ProgressOut(topic_id=r.topic_id, completed=r.completed_once, next_set_index=r.next_set_index)
        for r in rows
    ]
