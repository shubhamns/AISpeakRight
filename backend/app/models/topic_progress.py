from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base

class TopicProgress(Base):
    __tablename__ = "topic_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    topic_id = Column(String, index=True)
    next_set_index = Column(Integer, default=0)
    completed_once = Column(Boolean, default=False)
