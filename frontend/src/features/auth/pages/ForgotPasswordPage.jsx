import { useState } from "react";
import { Link } from "react-router-dom";
import { apiForgotPassword } from "@/shared/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");
  const [token, setToken] = useState(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setMsg("");
    setToken(null);
    setBusy(true);
    try {
      const out = await apiForgotPassword(email.trim());
      setMsg(out.message || "");
      if (out.reset_token) setToken(out.reset_token);
    } catch (x) {
      setErr(x.message || "Request failed");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="auth-page">
      <div className="glass-panel auth-panel">
        <h2>Reset password</h2>
        <p className="auth-sub">We will email instructions if the account exists.</p>
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
          {err ? <p className="err">{err}</p> : null}
          {msg ? <p className="auth-msg">{msg}</p> : null}
          {token ? (
            <p className="auth-dev-token">
              Dev token: <code>{token}</code>
              <br />
              <Link to={`/reset-password?token=${encodeURIComponent(token)}`}>Open reset page</Link>
            </p>
          ) : null}
          <button type="submit" className="btn auth-submit" disabled={busy}>
            {busy ? "Sending…" : "Send link"}
          </button>
        </form>
        <p className="auth-links">
          <Link to="/login">Back to sign in</Link>
        </p>
      </div>
    </div>
  );
}
