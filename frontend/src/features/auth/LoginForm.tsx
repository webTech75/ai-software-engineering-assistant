import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthContext";
import { AuthBackground } from "@/components/common/AuthBackground";
import { RobotMascot } from "@/components/common/RobotMascot";
import { login } from "./auth";

export function LoginForm() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");

    if (!username.trim()) {
      setError("Username is required.");
      return;
    }

    if (!password.trim()) {
      setError("Password is required.");
      return;
    }

    try {
      setLoading(true);

      await login(username, password);
      await refreshUser();

      setUsername("");
      setPassword("");

      navigate("/", { replace: true });
    } catch (err) {
      console.error(err);
      setError("Invalid username or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center p-4">
      <AuthBackground />
     
      <div className="auth-card relative z-10 w-full max-w-md rounded-2xl p-8">
        <div className="mb-8 text-center">
          <div className="mb-3 text-4xl">
             <RobotMascot mood={"idle"} />
          </div>
          <h1 className="bg-gradient-to-r from-primary to-chart-2 bg-clip-text text-3xl font-bold text-transparent">
            AI Software Engineering Assistant
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Your AI Pair Programmer
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="mb-2 block text-sm font-medium">
              Username
            </label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 outline-none focus:border-primary"
            />
          </div>

          <div>
            <label htmlFor="password" className="mb-2 block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 outline-none focus:border-primary"
            />
          </div>

          {error && (
            <p className="text-sm text-destructive" role="alert">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full py-2.5 font-medium disabled:opacity-50"
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}