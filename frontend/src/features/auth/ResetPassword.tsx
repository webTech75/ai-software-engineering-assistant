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
                navigate("/login");
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
        <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">

            <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">

                <h1 className="text-3xl font-bold text-center text-slate-900">
                    Reset Password
                </h1>

                <p className="mt-2 text-center text-slate-500">
                    Create a new password for your account.
                </p>

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

                            <label className="mb-2 block text-sm font-medium text-slate-700">
                                New Password
                            </label>

                            <input
                                type="password"
                                value={password}
                                onChange={(e) => {
                                    setPassword(e.target.value)
                                    setError("");
                                }}
                                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                            />

                        </div>

                        <div>

                            <label className="mb-2 block text-sm font-medium text-slate-700">
                                Confirm Password
                            </label>

                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => {
                                    setConfirmPassword(e.target.value)
                                    setError("");
                                }}
                                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                            />

                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {loading ? "Resetting..." : "Reset Password"}
                        </button>

                    </form>

                )}

            </div>

        </div>
    );
}