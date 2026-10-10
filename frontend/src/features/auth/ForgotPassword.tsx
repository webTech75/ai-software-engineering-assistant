import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { AuthBackground } from "@/components/common/AuthBackground";
import { RobotMascot } from "@/components/common/RobotMascot";
import { forgotPassword } from "./auth";

export function ForgotPassword() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();


        if (error) setError("");
        if (success) setSuccess("");

        if (!email.trim()) {
            setError("Email is required.");
            return;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            setError("Please enter a valid email address.");
            return;
        }

        try {
            setLoading(true);

            await forgotPassword(email);
            setError("");
            setSuccess(
                "If an account exists, a password reset link has been sent."
            );

            setEmail("");

            setSuccess(
                "If an account exists, a password reset link will be sent."
            );

            setEmail("");

        } catch (err) {
            console.error(err);

            setError("Unable to process your request.");

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
                        <RobotMascot mood="idle" />
                    </div>

                    <h1 className="bg-gradient-to-r from-primary to-chart-2 bg-clip-text text-3xl font-bold text-transparent">
                        Forgot Password
                    </h1>

                    <p className="mt-2 text-sm text-muted-foreground">
                        Enter your email address to reset your password.
                    </p>

                </div>

                <form
                    onSubmit={handleSubmit}
                    className="space-y-4"
                >

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
                                if (success) setSuccess("");
                                if (error) setError("");
                            }}
                            className="w-full px-3 py-2 outline-none focus:border-primary"
                        />

                    </div>

                    {error && (
                        <p
                            className="text-sm text-destructive"
                            role="alert"
                        >
                            {error}
                        </p>
                    )}

                    {success && (
                        <p
                            className="text-sm text-green-600"
                            role="status"
                        >
                            {success}
                        </p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-primary w-full py-2.5 font-medium disabled:opacity-50"
                    >
                        {loading
                            ? "Sending..."
                            : "Send Reset Link"}
                    </button>

                    <button
                        type="button"
                        onClick={() => navigate("/login")}
                        className="w-full text-sm text-primary hover:underline"
                    >
                        Back to Sign In
                    </button>

                </form>

            </div>

        </div>
    );
}