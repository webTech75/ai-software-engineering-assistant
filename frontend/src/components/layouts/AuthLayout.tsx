import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <Outlet />
    </main>
  );
}