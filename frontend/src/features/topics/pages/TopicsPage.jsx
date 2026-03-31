import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchTopics } from "@/shared/api";

export default function TopicsPage() {
  const { levelId } = useParams();
  const [topics, setTopics] = useState([]);
  const [err, setErr] = useState(null);
  useEffect(() => {
    fetchTopics(levelId)
      .then(setTopics)
      .catch((e) => setErr(e.message));
  }, [levelId]);
  if (err) return <p className="err">{err}</p>;
  const title =
    levelId === "beginner"
      ? "Beginner"
      : levelId === "intermediate"
        ? "Intermediate"
        : levelId === "advanced"
          ? "Advanced"
          : levelId;
  return (
    <>
      <Link className="back" to="/">
        ← Levels
      </Link>
      <h2>{title} topics</h2>
      <p className="lead">Open a topic to learn and take a short exam.</p>
      <div className="grid">
        {topics.map((t) => (
          <Link key={t.id} className="card" to={`/topic/${t.id}`}>
            <strong>{t.title}</strong>
            {t.completed && <span className="badge">Completed</span>}
          </Link>
        ))}
      </div>
    </>
  );
}
