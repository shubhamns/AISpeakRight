import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  apiLogin,
  apiRegister,
  clearAccessToken,
  fetchMe,
  getAccessToken,
  setAccessToken,
} from "@/shared/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const t = getAccessToken();
    if (!t) {
      setReady(true);
      return;
    }
    fetchMe()
      .then(setUser)
      .catch(() => {
        clearAccessToken();
        setUser(null);
      })
      .finally(() => setReady(true));
  }, []);
  const login = useCallback(async (email, password) => {
    const { access_token } = await apiLogin(email, password);
    setAccessToken(access_token);
    const u = await fetchMe();
    setUser(u);
  }, []);
  const register = useCallback(async (email, password) => {
    const { access_token } = await apiRegister(email, password);
    setAccessToken(access_token);
    const u = await fetchMe();
    setUser(u);
  }, []);
  const logout = useCallback(() => {
    clearAccessToken();
    setUser(null);
  }, []);
  const value = useMemo(
    () => ({ user, ready, login, register, logout }),
    [user, ready, login, register, logout]
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth outside AuthProvider");
  return ctx;
}
