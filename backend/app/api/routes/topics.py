from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.content import TOPICS_BY_ID, TOPICS_LIST
from app.models.user import User
from app.schemas import TopicDetail, TopicSummary
from app.services.progress_service import get_or_create_progress

router = APIRouter()

def _uid(user: User) -> str:
    return str(user.id)

@router.get("/topics", response_model=list[TopicSummary])
def list_topics(level_id: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    out = []
    uid = _uid(current_user)
    for t in TOPICS_LIST:
        if t["level_id"] != level_id:
            continue
        prog = get_or_create_progress(db, uid, t["id"])
        out.append(
            TopicSummary(
                id=t["id"],
                level_id=t["level_id"],
                title=t["title"],
                completed=prog.completed_once,
            )
        )
    return out

@router.get("/topics/{topic_id}", response_model=TopicDetail)
def get_topic(topic_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if topic_id not in TOPICS_BY_ID:
        raise HTTPException(404, "Topic not found")
    t = TOPICS_BY_ID[topic_id]
    prog = get_or_create_progress(db, _uid(current_user), topic_id)
    return TopicDetail(
        id=t["id"],
        level_id=t["level_id"],
        title=t["title"],
        explanation=t["explanation"],
        examples=t["examples"],
        completed=prog.completed_once,
        total_question_sets=len(t["question_sets"]),
        next_set_index=prog.next_set_index,
    )
