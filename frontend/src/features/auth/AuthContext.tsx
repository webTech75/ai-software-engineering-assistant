import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getCurrentUser, logout as clearAuth, storage } from "./auth";

const AuthContext = createContext<any>(null);

export function AuthProvider({ children}: { children: ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  async function refreshUser() {
    if (!storage.getToken()) {
      setUser(null);
      return;
    }

    try {
      setUser(await getCurrentUser());
    } catch {
      setUser(null);
      throw new Error("Failed to load user");
    }
  }

  function logout() {
    clearAuth();
    setUser(null);
  }

  useEffect(() => {
    refreshUser()
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, refreshUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}