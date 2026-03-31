import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/shared/context/AuthContext.jsx";

export default function RequireAuth() {
  const { user, ready } = useAuth();
  const loc = useLocation();
  if (!ready) return <div className="page-loading" aria-busy="true" />;
  if (!user) return <Navigate to="/login" state={{ from: loc }} replace />;
  return <Outlet />;
}
