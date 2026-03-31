from pydantic import BaseModel

class LevelOut(BaseModel):
    id: str
    name: str
