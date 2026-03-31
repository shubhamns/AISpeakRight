import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchLevels } from "@/shared/api";

export default function LevelsPage() {
  const [levels, setLevels] = useState([]);
  const [err, setErr] = useState(null);
  useEffect(() => {
    fetchLevels()
      .then(setLevels)
      .catch((e) => setErr(e.message));
  }, []);
  if (err) return <p className="err">{err}</p>;
  return (
    <>
      <h2>Choose your level</h2>
      <p className="lead">Pick a level to see topics and practice real English.</p>
      <div className="grid">
        {levels.map((l) => (
          <Link key={l.id} className="card" to={`/level/${l.id}`}>
            <strong>{l.name}</strong>
          </Link>
        ))}
      </div>
    </>
  );
}
