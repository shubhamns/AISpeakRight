import { Link } from "react-router-dom";
import { useState } from "react";
import { correctSentence } from "@/shared/api";

export default function PracticePage() {
  const [text, setText] = useState("");
  const [out, setOut] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);
  const go = () => {
    const s = text.trim();
    if (!s) return;
    setErr(null);
    setLoading(true);
    setOut(null);
    correctSentence(s)
      .then(setOut)
      .catch((e) => setErr(e.message))
      .finally(() => setLoading(false));
  };
  return (
    <>
      <Link className="back" to="/">
        ← Home
      </Link>
      <h2>Free practice</h2>
      <p className="lead">Type any sentence. We correct it and explain in simple words.</p>
      <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="e.g. I do a car" />
      <div className="btn-row">
        <button type="button" className="btn" disabled={loading} onClick={go}>
          {loading ? "…" : "Check"}
        </button>
      </div>
      {err && <p className="err">{err}</p>}
      {out && (
        <div className="result-box pass" style={{ marginTop: "1rem" }}>
          <p style={{ margin: 0 }}>
            <strong>Correct:</strong> {out.correct}
          </p>
          <p style={{ margin: "0.75rem 0 0" }}>
            <strong>Why:</strong> {out.explanation}
          </p>
        </div>
      )}
    </>
  );
}
