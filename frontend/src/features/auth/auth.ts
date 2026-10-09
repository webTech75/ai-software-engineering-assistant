import {
  loginRequest,
  getCurrentUserRequest,
} from "@/api/requests";

const TOKEN_KEY = "access_token";

export const storage = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  setToken(token: string) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },
};

export function logout(): void {
  storage.removeToken();
}

export async function login(username: string, password: string) {
  const data = await loginRequest(username, password);
  storage.setToken(data.access_token);
  return data;
}

export async function getCurrentUser() {
  return await getCurrentUserRequest();
}