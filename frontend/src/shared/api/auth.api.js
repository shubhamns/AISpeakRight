import { publicRequest, request } from "./httpClient.js";

export function apiRegister(email, password) {
  return publicRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function apiLogin(email, password) {
  return publicRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function apiForgotPassword(email) {
  return publicRequest("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export function apiResetPassword(token, password) {
  return publicRequest("/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({ token, password }),
  });
}

export function fetchMe() {
  return request("/auth/me");
}
