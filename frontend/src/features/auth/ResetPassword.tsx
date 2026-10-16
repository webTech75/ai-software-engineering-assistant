import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { resetPassword } from "./auth";

export function ResetPassword() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate(); 
    const token = searchParams.get("token");

    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (
        e: React.FormEvent<HTMLFormElement>
    ) => {
        e.preventDefault();

        setError("");
        setSuccess("");

        if (!token) {
            setError("Invalid password reset link.");
            return;
        }

        if (!password.trim()) {
            setError("Please enter a new password.");
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
        setLoading(true);

        try {

            await resetPassword(token, password);
            setSuccess("Password reset successfully. Redirecting to the login page...");
            setPassword("");
            setConfirmPassword("");
            setTimeout(() => {
                navigate("/");
            }, 2000);
        } catch(err: any) {
            setError(
                err.response?.data?.detail ??
                "Unable to reset your password."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-card relative z-10 w-full max-w-md rounded-2xl p-8">   

           <div className="mb-8 text-center">
                <h1 className="bg-gradient-to-r from-primary to-chart-2 bg-clip-text text-3xl font-bold text-transparent">
                    Reset Password
                </h1>

                <p className="mt-2 text-sm text-muted-foreground">
                    Create a new password for your account.
                </p>
            </div>

            {error && (
                <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-3 text-red-700">
                    {error}
                </div>
            )}

            {success && (
                <div className="mt-6 rounded-lg border border-green-200 bg-green-50 p-3 text-green-700">
                    {success}
                </div>
            )}

            {!token ? (

                <div className="mt-6">

                    <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-red-700">
                        Invalid password reset link.
                    </div>

                </div>

            ) : (

                <form
                    onSubmit={handleSubmit}
                    className="mt-6 space-y-5"
                >

                    <div>

                        <label className="mb-2 block text-sm font-medium">
                            New Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(e) => {
                                setPassword(e.target.value)
                                setError("");
                            }}
                            className="w-full px-3 py-2 outline-none focus:border-primary"
                        />

                    </div>

                    <div>

                        <label className="mb-2 block text-sm font-medium">
                            Confirm Password
                        </label>

                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => {
                                setConfirmPassword(e.target.value)
                                setError("");
                            }}
                            className="w-full px-3 py-2 outline-none focus:border-primary"
                        />

                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-primary w-full py-2.5 font-medium disabled:opacity-50">
                        {loading ? "Resetting..." : "Reset Password"}
                    </button>

                </form>

            )}

        </div>
    );
}