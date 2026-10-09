import { useNavigate } from "react-router-dom";

import { useAuth } from "@/features/auth/AuthContext";
import { Logo } from "@/components/common/Logo";
import { ThemeSwitcher } from "@/components/common/ThemeSwitcher";


export function Header() {
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="flex h-16 items-center justify-between border-b px-6">
      <Logo />
      <div className="flex items-center gap-3">
         {user && (
          <span className="text-sm font-semibold uppercase">
           Welcome, {user.username}
          </span>
        )}
          <ThemeSwitcher />
          <button onClick={handleLogout}>
            Logout
          </button>
        </div>
    </header>
  );
}