import { Navigate } from 'react-router-dom'

import { storage } from '@/components/auth/auth'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute ({ children }: ProtectedRouteProps) {
  const token = storage.getToken()

  if (!token) {
    return <Navigate to='/' replace />
  }

  return <>{children}</>
}
