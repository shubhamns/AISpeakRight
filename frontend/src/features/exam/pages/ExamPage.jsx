import { Link, useParams } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import { fetchExamQuestions, fetchTopicDetail, submitExam } from "@/shared/api";

export default function ExamPage() {
  const { topicId } = useParams();
  const [topicTitle, setTopicTitle] = useState("");
  const [levelId, setLevelId] = useState("");
  const [phase, setPhase] = useState("load");
  const [questions, setQuestions] = useState([]);
  const [setIndex, setSetIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [err, setErr] = useState(null);
  const load = useCallback(
    (retryIdx) => {
      setErr(null);
      setPhase("load");
      return fetchExamQuestions(topicId, retryIdx)
        .then((data) => {
          setQuestions(data.questions);
          setSetIndex(data.set_index);
          setAnswers({});
          setResult(null);
          setPhase("take");
        })
        .catch((e) => {
          setErr(e.message);
        });
    },
    [topicId]
  );
  useEffect(() => {
    fetchTopicDetail(topicId)
      .then((t) => {
        setTopicTitle(t.title);
        setLevelId(t.level_id);
      })
      .catch(() => {});
  }, [topicId]);
  useEffect(() => {
    load(undefined);
  }, [load]);
  const setAns = (id, v) => setAnswers((a) => ({ ...a, [id]: v }));
  const onSubmit = () => {
    const payload = questions.map((q) => ({
      question_id: q.id,
      answer: (answers[q.id] || "").trim(),
    }));
    submitExam(topicId, setIndex, payload)
      .then((r) => {
        setResult(r);
        setPhase("result");
      })
      .catch((e) => setErr(e.message));
  };
  if (err && phase === "load") return <p className="err">{err}</p>;
  if (phase === "load") return <p>Loading exam…</p>;
  if (phase === "result" && result) {
    const pct = Math.round((result.score / result.total) * 100);
    if (!result.passed) {
      return (
        <>
          <Link className="back" to={`/topic/${topicId}`}>
            ← Topic
          </Link>
          <h2>{topicTitle}</h2>
          <div className="result-box fail">
            <strong>You failed. Try again</strong>
            <p style={{ margin: "0.5rem 0 0" }}>
              Score: {result.score}/{result.total} ({pct}%)
            </p>
            <p className="lead" style={{ marginTop: "0.75rem" }}>
              You need at least 70% to pass.
            </p>
            <div className="btn-row">
              <button
                type="button"
                className="btn"
                onClick={() => {
                  load(result.set_index);
                }}
              >
                Retry
              </button>
              <Link className="btn secondary" to={`/topic/${topicId}`}>
                Back to topic
              </Link>
            </div>
          </div>
        </>
      );
    }
    return (
      <>
        <Link className="back" to={`/topic/${topicId}`}>
          ← Topic
        </Link>
        <h2>{topicTitle}</h2>
        <div className="result-box pass">
          <strong>Topic completed</strong>
          <p style={{ margin: "0.5rem 0 0" }}>
            Score: {result.score}/{result.total} ({pct}%)
          </p>
          {result.total_question_sets > 1 && (
            <p className="lead" style={{ marginTop: "0.5rem" }}>
              Set {result.set_index + 1} of {result.total_question_sets}
            </p>
          )}
          <div className="btn-row">
            {result.has_next_set && (
              <button type="button" className="btn" onClick={() => load(result.set_index + 1)}>
                Next question set
              </button>
            )}
            <Link className="btn secondary" to={`/level/${levelId}`}>
              Back to topics
            </Link>
          </div>
          {!result.has_next_set && result.total_question_sets > 1 && (
            <p className="lead" style={{ marginTop: "0.75rem" }}>
              You finished all question sets for this topic.
            </p>
          )}
        </div>
      </>
    );
  }
  return (
    <div className="page-sticky-foot">
      <Link className="back" to={`/topic/${topicId}`}>
        ← Topic
      </Link>
      <h2>Exam: {topicTitle}</h2>
      <p className="lead">15 questions. Fill in, choose, or pick the best sentence.</p>
      {err && <p className="err">{err}</p>}
      {questions.map((q) => (
        <div key={`${setIndex}-${q.id}`} className="q-block">
          <label className="prompt">{q.prompt}</label>
          {q.type === "fill_blank" && (
            <input
              type="text"
              value={answers[q.id] || ""}
              onChange={(e) => setAns(q.id, e.target.value)}
              placeholder="Your answer"
            />
          )}
          {(q.type === "mcq" || q.type === "correction") && q.options && (
            <div className="opts">
              {q.options.map((opt) => (
                <label key={opt}>
                  <input
                    type="radio"
                    name={q.id}
                    checked={(answers[q.id] || "") === opt}
                    onChange={() => setAns(q.id, opt)}
                  />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      ))}
      <div className="sticky-bottom-bar" role="region" aria-label="Submit exam">
        <div className="sticky-bottom-bar__inner">
          <button type="button" className="btn" onClick={onSubmit}>
            Submit
          </button>
        </div>
      </div>
    </div>
  );
}
