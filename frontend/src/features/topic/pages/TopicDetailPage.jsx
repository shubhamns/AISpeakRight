import { Link, useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchTopicDetail } from "@/shared/api";

export default function TopicDetailPage() {
  const { topicId } = useParams();
  const nav = useNavigate();
  const [t, setT] = useState(null);
  const [err, setErr] = useState(null);
  useEffect(() => {
    fetchTopicDetail(topicId)
      .then(setT)
      .catch((e) => setErr(e.message));
  }, [topicId]);
  if (err) return <p className="err">{err}</p>;
  if (!t) return <p>Loading…</p>;
  return (
    <>
      <Link className="back" to={`/level/${t.level_id}`}>
        ← Topics
      </Link>
      <h2>{t.title}</h2>
      <p className="lead">{t.explanation}</p>
      <h3 style={{ fontSize: "1rem", margin: "1rem 0 0.5rem" }}>Examples</h3>
      {t.examples.map((ex, i) => (
        <div key={i} className="ex">
          {ex}
        </div>
      ))}
      <div className="btn-row">
        <button type="button" className="btn secondary" onClick={() => nav(`/topic/${topicId}/learn`)}>
          Start Learning
        </button>
        <button type="button" className="btn" onClick={() => nav(`/topic/${topicId}/exam`)}>
          Start Exam
        </button>
      </div>
    </>
  );
}
