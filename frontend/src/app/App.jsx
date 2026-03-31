import { BrowserRouter, Link, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "@/shared/context/AuthContext.jsx";
import { AppRoutes } from "./routes.jsx";
import "./App.css";

function Shell() {
  const { user, logout } = useAuth();
  const loc = useLocation();
  const authRoute =
    /^\/(login|register|forgot-password|reset-password)(\/|$)/.test(loc.pathname);
  return (
    <div className="app">
      {!authRoute ? (
        <header className="glass-header">
          <h1>Smart English Coach</h1>
          <div className="header-actions">
            <nav>
              <Link to="/">Home</Link>
              {" · "}
              <Link to="/practice">Practice</Link>
            </nav>
            {user ? (
              <span className="user-pill">
                <span className="user-email">{user.email}</span>
                <button type="button" className="btn ghost" onClick={logout}>
                  Log out
                </button>
              </span>
            ) : null}
          </div>
        </header>
      ) : null}
      <AppRoutes />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Shell />
      </AuthProvider>
    </BrowserRouter>
  );
}
