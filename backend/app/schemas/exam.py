from typing import Literal, Optional
from pydantic import BaseModel

class QuestionOut(BaseModel):
    id: str
    type: Literal["fill_blank", "mcq", "correction"]
    prompt: str
    options: Optional[list[str]] = None

class ExamQuestionsResponse(BaseModel):
    topic_id: str
    set_index: int
    questions: list[QuestionOut]

class AnswerIn(BaseModel):
    question_id: str
    answer: str

class ExamSubmitIn(BaseModel):
    topic_id: str
    set_index: int
    answers: list[AnswerIn]

class ExamSubmitOut(BaseModel):
    score: int
    total: int
    passed: bool
    set_index: int
    topic_id: str
    total_question_sets: int = 1
    has_next_set: bool = False
