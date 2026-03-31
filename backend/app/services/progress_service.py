from sqlalchemy.orm import Session
from app.models import TopicProgress

def get_or_create_progress(db: Session, user_id: str, topic_id: str) -> TopicProgress:
    row = db.query(TopicProgress).filter(
        TopicProgress.user_id == user_id,
        TopicProgress.topic_id == topic_id,
    ).first()
    if not row:
        row = TopicProgress(user_id=user_id, topic_id=topic_id, next_set_index=0, completed_once=False)
        db.add(row)
        db.commit()
        db.refresh(row)
    return row
