import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { apiResetPassword } from "@/shared/api";

export default function ResetPasswordPage() {
  const [sp] = useSearchParams();
  const initial = sp.get("token") || "";
  const [token, setToken] = useState(initial);
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setMsg("");
    setBusy(true);
    try {
      const out = await apiResetPassword(token.trim(), password);
      setMsg(out.message || "Done");
    } catch (x) {
      setErr(x.message || "Reset failed");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="auth-page">
      <div className="glass-panel auth-panel">
        <h2>New password</h2>
        <p className="auth-sub">Paste the reset token from your email (or dev link).</p>
        <form onSubmit={onSubmit} className="auth-form">
          <label className="field">
            <span>Reset token</span>
            <input
              type="text"
              autoComplete="off"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              required
            />
          </label>
          <label className="field">
            <span>New password</span>
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
          {msg ? <p className="auth-msg ok">{msg}</p> : null}
          <button type="submit" className="btn auth-submit" disabled={busy}>
            {busy ? "Updating…" : "Update password"}
          </button>
        </form>
        <p className="auth-links">
          <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
