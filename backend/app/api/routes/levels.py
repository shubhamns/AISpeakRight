from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.content import LEVELS
from app.models.user import User
from app.schemas import LevelOut

router = APIRouter()

@router.get("/levels", response_model=list[LevelOut])
def list_levels(_: User = Depends(get_current_user)):
    return [LevelOut(**x) for x in LEVELS]
