import random
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.content import TOPICS_BY_ID
from app.models.user import User
from app.schemas import ExamQuestionsResponse, ExamSubmitIn, ExamSubmitOut
from app.services.exam_service import (
    build_submit_result,
    evaluate_submission,
    question_to_response,
)
from app.services.progress_service import get_or_create_progress

router = APIRouter()

def _uid(user: User) -> str:
    return str(user.id)

@router.get("/exam/questions", response_model=ExamQuestionsResponse)
def get_questions(
    topic_id: str = Query(...),
    retry_set_index: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if topic_id not in TOPICS_BY_ID:
        raise HTTPException(404, "Topic not found")
    t = TOPICS_BY_ID[topic_id]
    sets = t["question_sets"]
    n = len(sets)
    if n == 0:
        raise HTTPException(400, "No questions")
    uid = _uid(current_user)
    if retry_set_index is not None:
        si = max(0, min(retry_set_index, n - 1))
    else:
        prog = get_or_create_progress(db, uid, topic_id)
        si = min(prog.next_set_index, n - 1)
    qs = list(sets[si])
    random.shuffle(qs)
    return ExamQuestionsResponse(
        topic_id=topic_id,
        set_index=si,
        questions=[question_to_response(q) for q in qs],
    )

@router.post("/exam/submit", response_model=ExamSubmitOut)
def submit(
    body: ExamSubmitIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if body.topic_id not in TOPICS_BY_ID:
        raise HTTPException(404, "Topic not found")
    t = TOPICS_BY_ID[body.topic_id]
    sets = t["question_sets"]
    if body.set_index < 0 or body.set_index >= len(sets):
        raise HTTPException(400, "Invalid set index")
    score, total, passed = evaluate_submission(t, body.set_index, body.answers)
    n_sets = len(sets)
    has_next = passed and (body.set_index + 1 < n_sets)
    uid = _uid(current_user)
    prog = get_or_create_progress(db, uid, body.topic_id)
    if passed:
        prog.completed_once = True
        prog.next_set_index = min(body.set_index + 1, n_sets - 1)
        db.commit()
        db.refresh(prog)
    return build_submit_result(
        score,
        total,
        passed,
        body.set_index,
        body.topic_id,
        total_question_sets=n_sets,
        has_next_set=has_next,
    )
