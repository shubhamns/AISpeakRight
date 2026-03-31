from pydantic import BaseModel, Field

class PracticeIn(BaseModel):
    sentence: str = Field(..., min_length=1, max_length=500)

class PracticeOut(BaseModel):
    correct: str
    explanation: str
