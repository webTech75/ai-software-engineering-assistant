import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthContext";
import { AuthBackground } from "@/components/common/AuthBackground";
import { RobotMascot } from "@/components/common/RobotMascot";
import { login, register } from "./auth";

type AuthMode = "login" | "register";

export function LoginForm() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mode, setMode] = useState<AuthMode>("login");
  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");

    if (!username.trim()) {
      setError("Username is required.");
      return;
    }
    if (username.length < 3) {
          setError("Username must be at least 3 characters.");
          return;
      }


    if (!password.trim()) {
      setError("Password is required.");
      return;
    }
    if (password.length < 8) {
          setError("Password must be at least 8 characters long.");
          return;
      }


    if (mode === "register") {
      if (username.length < 3) {
            setError("Username must be at least 3 characters.");
            return;
        }

        if (username.length > 30) {
            setError("Username cannot exceed 30 characters.");
            return;
        }

        const usernameRegex = /^[A-Za-z][A-Za-z0-9_]*$/;

        if (!usernameRegex.test(username)) {
            setError(
                "Username must start with a letter and contain only letters, numbers, and underscores."
            );
            return;
        }

        if (!email.trim()) {
            setError("Email is required.");
            return;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            setError("Please enter a valid email address.");
            return;
        }

        if (password.length < 8) {
            setError("Password must be at least 8 characters long.");
            return;
        }

        if (!confirmPassword.trim()) {
            setError("Please confirm your password.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }
    }

    try {
        setLoading(true);

        if (mode === "login") {
            await login(username, password);
            await refreshUser();
            setUsername("");
            setPassword("");
            navigate("/", { replace: true });
        } else {
            await register(username, email, password);
            setSuccess("Account created successfully. Please sign in.");
            setMode("login");
            setPassword("");
            setUsername("");
            setEmail("");
            setConfirmPassword("");
        }

    } catch (err) {
        console.error(err);
        setError(
            mode === "login"
                ? "Invalid username or password."
                : "Unable to create account."
        );

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
            {mode === "login"
                ? "AI Software Engineering Assistant"
                : "Create Your Account"}
        </h1>

        <p className="mt-2 text-sm text-muted-foreground">
            {mode === "login"
                ? "Your AI Pair Programmer"
                : "Join your AI Pair Programmer"}
        </p>
        </div>

        <div className="mb-6 flex rounded-lg border border-border p-1">

            <button
              type="button"
              onClick={() => {
                setMode("login");
                setError("");
              }}
              className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-all ${
                mode === "login"
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted"
              }`}
            >
              Sign In
            </button>

            <button
              type="button"
              onClick={() => {
                setMode("register");
                setPassword("");
                setUsername("");
                setError("");
              }}
              className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-all ${
                mode === "register"
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted"
              }`}
            >
              Register
            </button>

          </div>

        <form onSubmit={handleSubmit} className="space-y-4 transition-all duration-300">
          <div>
            <label htmlFor="username" className="mb-2 block text-sm font-medium">
              Username
            </label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value);
                setError("");
                setSuccess('')
              }}
              className="w-full px-3 py-2 outline-none focus:border-primary"
            />
          </div>

            {mode === "register" && (
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-medium"
                >
                  Email
                </label>

                <input
                  id="email"
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setError("");
                  }}
                  className="w-full px-3 py-2 outline-none focus:border-primary"
                />
              </div>
            )}
          <div>

            <label htmlFor="password" className="mb-2 block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError("");
              }}
              className="w-full px-3 py-2 outline-none focus:border-primary"
            />
          </div>
           {mode === "login" && (
              <div className="mt-2 flex justify-end">
                <button
                  type="button"
                  onClick={() => navigate("/forgot-password")}
                  className="text-sm text-primary transition-colors hover:underline"
                >
                  Forgot Password?
                </button>
              </div>
            )}

             {mode === "register" && (
              <div>
                <label
                  htmlFor="confirmPassword"
                  className="mb-2 block text-sm font-medium"
                >
                  Confirm Password
                </label>

                <input
                  id="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value);
                    setError("");
                  }}
                  className="w-full px-3 py-2 outline-none focus:border-primary"
                />
              </div>
            )}

          {success && (
            <p className="text-sm text-green-600" role="status">
              {success}
            </p>
          )}
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
            {loading
              ? mode === "login"
                ? "Signing In..."
                : "Creating Account..."
              : mode === "login"
                ? "Sign In"
                : "Create Account"}
          </button>
        </form>
      </div>
    </div>
  );
}