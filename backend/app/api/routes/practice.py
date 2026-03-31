from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas import PracticeIn, PracticeOut
from app.services.practice_service import correct_sentence_ai

router = APIRouter()

@router.post("/practice/correct", response_model=PracticeOut)
def correct(body: PracticeIn, _: User = Depends(get_current_user)):
    return correct_sentence_ai(body.sentence)
