import { Navigate } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthContext";
import { LoginForm } from "@/features/auth/LoginForm";

export function Login() {
  const { user, loading } = useAuth();

  if (loading) {
    return <p>Loading...</p>;
  }

  if (user) {
    return <Navigate to="/" replace />;
  }

  return <LoginForm />;
}