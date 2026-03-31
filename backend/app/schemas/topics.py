from pydantic import BaseModel

class TopicSummary(BaseModel):
    id: str
    level_id: str
    title: str
    completed: bool = False

class TopicDetail(BaseModel):
    id: str
    level_id: str
    title: str
    explanation: str
    examples: list[str]
    completed: bool = False
    total_question_sets: int
    next_set_index: int
