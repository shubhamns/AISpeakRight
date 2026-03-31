from app.content import grade_answer
from app.schemas import ExamSubmitOut, QuestionOut

def question_to_response(q: dict) -> QuestionOut:
    return QuestionOut(
        id=q["id"],
        type=q["type"],
        prompt=q["prompt"],
        options=q.get("options"),
    )

def evaluate_submission(topic: dict, set_index: int, answers: list) -> tuple[int, int, bool]:
    sets = topic["question_sets"]
    qs = sets[set_index]
    by_id = {q["id"]: q for q in qs}
    total = len(qs)
    score = 0
    for a in answers:
        q = by_id.get(a.question_id)
        if q and grade_answer(q, a.answer):
            score += 1
    passed = total > 0 and (score / total) >= 0.70
    return score, total, passed

def build_submit_result(
    score: int,
    total: int,
    passed: bool,
    set_index: int,
    topic_id: str,
    *,
    total_question_sets: int = 1,
    has_next_set: bool = False,
) -> ExamSubmitOut:
    return ExamSubmitOut(
        score=score,
        total=total,
        passed=passed,
        set_index=set_index,
        topic_id=topic_id,
        total_question_sets=total_question_sets,
        has_next_set=has_next_set,
    )
