import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { AuthProvider } from '@/features/auth/AuthContext';
import "./index.css";

import { router } from "@/router";
import { setTheme, getTheme } from "@/utils/theme/theme";

// Initialize the theme on page load
setTheme(getTheme());

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </React.StrictMode>
);