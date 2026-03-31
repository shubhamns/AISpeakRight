import { API_BASE_URL } from "./config.js";
import { clearAccessToken, getAccessToken } from "../lib/authStorage.js";

function detailMessage(detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((x) => x.msg || JSON.stringify(x)).join(", ");
  return JSON.stringify(detail);
}

async function parseResponse(r) {
  const text = await r.text();
  let msg = text || r.statusText;
  if (!r.ok) {
    try {
      const j = JSON.parse(text);
      if (j.detail !== undefined) msg = detailMessage(j.detail);
    } catch {
      /* keep msg */
    }
    const token = getAccessToken();
    if (r.status === 401 && token) {
      clearAccessToken();
      const p = window.location.pathname;
      if (!p.startsWith("/login") && !p.startsWith("/register") && !p.startsWith("/forgot-password") && !p.startsWith("/reset-password")) {
        window.location.href = "/login";
      }
    }
    throw new Error(msg);
  }
  if (!text) return null;
  return JSON.parse(text);
}

export async function request(path, opts = {}) {
  const token = getAccessToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...opts.headers,
  };
  const r = await fetch(`${API_BASE_URL}${path}`, { ...opts, headers });
  return parseResponse(r);
}

export async function publicRequest(path, opts = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...opts.headers,
  };
  const r = await fetch(`${API_BASE_URL}${path}`, { ...opts, headers });
  return parseResponse(r);
}
