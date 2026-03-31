import { useState } from "react";
import { Link, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/shared/context/AuthContext.jsx";

export default function LoginPage() {
  const { user, ready, login } = useAuth();
  const loc = useLocation();
  const from = loc.state?.from?.pathname || "/";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  if (ready && user) return <Navigate to={from} replace />;
  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setBusy(true);
    try {
      await login(email.trim(), password);
    } catch (x) {
      setErr(x.message || "Sign in failed");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="auth-page">
      <div className="auth-page__header">
        <h1 className="auth-page__title">Smart English Coach</h1>
        <p className="auth-page__desc">
          Learn English grammar by level, take short exams, and fix sentences with instant feedback—all in one place.
        </p>
      </div>
      <div className="glass-panel auth-panel">
        <h2>Sign in</h2>
        <p className="auth-sub">Use your email and password to continue.</p>
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
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          {err ? <p className="err">{err}</p> : null}
          <button type="submit" className="btn auth-submit" disabled={busy}>
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="auth-links">
          <Link to="/forgot-password">Forgot password?</Link>
          {" · "}
          <Link to="/register">Create account</Link>
        </p>
      </div>
    </div>
  );
}
