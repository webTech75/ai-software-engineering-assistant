import { createBrowserRouter } from 'react-router-dom'

import { AppLayout } from '@/components/layouts/AppLayout'
import { AuthLayout } from '@/components/layouts/AuthLayout'
import { Dashboard } from '@/components/dashboard/Dashboard'
import { NotFound } from '@/components/common/NotFound'
import { ProtectedRoute } from './ProtectedRoute'
import { Project } from '@/components/projectWorkspace/Project'
import { ResetPassword } from '@/components/auth/ResetPassword'
import { Landing } from '@/components/landing/Landing'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Landing />
  },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: '/dashboard',
        element: <Dashboard />
      },
      {
        path: '/projects/:projectId',
        element: <Project />
      }
    ]
  },
  {
    element: <AuthLayout />,
    children: [
      {
        path: '/reset-password',
        element: <ResetPassword />
      }
    ]
  },
  {
    path: '*',
    element: <NotFound />
  }
])
