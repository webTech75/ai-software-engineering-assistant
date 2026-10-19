import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { AuthProvider } from '@/components/auth/AuthContext'
import './index.css'
import { Toaster } from 'sonner'
import { router } from '@/router'
import { setTheme, getTheme } from '@/utils/theme'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

// Initialize the theme on page load
setTheme(getTheme())

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
      <Toaster position='top-right' richColors duration={6000} />
    </QueryClientProvider>
  </React.StrictMode>
)
