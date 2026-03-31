import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchTopicDetail } from "@/shared/api";

export default function LearnPage() {
  const { topicId } = useParams();
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
    <div className="page-sticky-foot">
      <Link className="back" to={`/topic/${topicId}`}>
        ← Topic
      </Link>
      <h2>{t.title}</h2>
      <p className="lead">{t.explanation}</p>
      {t.examples.map((ex, i) => (
        <div key={i} className="ex">
          {ex}
        </div>
      ))}
      <div className="sticky-bottom-bar" role="region" aria-label="Start exam">
        <div className="sticky-bottom-bar__inner">
          <Link className="btn" to={`/topic/${topicId}/exam`}>
            Start Exam
          </Link>
        </div>
      </div>
    </div>
  );
}
