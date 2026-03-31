import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "@/shared/context/AuthContext.jsx";

export default function RegisterPage() {
  const { user, ready, register } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  if (ready && user) return <Navigate to="/" replace />;
  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setBusy(true);
    try {
      await register(email.trim(), password);
    } catch (x) {
      setErr(x.message || "Registration failed");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="auth-page">
      <div className="glass-panel auth-panel">
        <h2>Create account</h2>
        <p className="auth-sub">Start learning with your coach</p>
        <form onSubmit={onSubmit} className="auth-form">
          <label className="field">
            <span>Email</span>
            <input
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <label className="field">
            <span>Password</span>
            <input
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
          </label>
          {err ? <p className="err">{err}</p> : null}
          <button type="submit" className="btn auth-submit" disabled={busy}>
            {busy ? "Creating…" : "Register"}
          </button>
        </form>
        <p className="auth-links">
          <Link to="/login">Already have an account?</Link>
        </p>
      </div>
    </div>
  );
}
