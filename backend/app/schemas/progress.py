from pydantic import BaseModel

class ProgressOut(BaseModel):
    topic_id: str
    completed: bool
    next_set_index: int
