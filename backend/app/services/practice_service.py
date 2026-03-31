import json
from openai import OpenAI
from app.core.config import settings
from app.schemas import PracticeOut

def correct_sentence_ai(sentence: str) -> PracticeOut:
    s = sentence.strip()
    if not settings.openai_api_key:
        return PracticeOut(
            correct=s,
            explanation="Set OPENAI_API_KEY in backend/.env to enable AI corrections.",
        )
    client = OpenAI(api_key=settings.openai_api_key)
    msg = (
        f'Learner wrote: "{s}"\n'
        + 'Reply with JSON only: {"correct":"<natural corrected sentence>","explanation":"<one very short simple line for a beginner>"}'
    )
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}],
            response_format={"type": "json_object"},
        )
        raw = r.choices[0].message.content or "{}"
        data = json.loads(raw)
        return PracticeOut(
            correct=str(data.get("correct", s)).strip(),
            explanation=str(data.get("explanation", "")).strip() or "No explanation returned.",
        )
    except Exception:
        return PracticeOut(correct=s, explanation="Could not reach AI. Check your API key and try again.")
