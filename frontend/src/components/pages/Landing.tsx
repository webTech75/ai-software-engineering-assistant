import { LandingHeader } from '@/components/landing/LandingHeader'
import { Hero } from '@/components/landing/Hero'
import { AuthBackground } from '@/components/common/AuthBackground'
import { useState } from 'react'
import { AuthCard } from '@/components/auth/AuthCard'
import { Navigate } from 'react-router-dom'
import { storage } from '@/components/auth/auth'

export function Landing () {
  const [showLogin, setShowLogin] = useState(false)

  const token = storage.getToken()

  if (token) {
    return <Navigate to='/dashboard' replace />
  }

  return (
    <main className='min-h-screen overflow-hidden bg-background'>
      <AuthBackground />

      {showLogin ? (
        <AuthCard />
      ) : (
        <>
          <LandingHeader onLogin={() => setShowLogin(true)} />

          <Hero />
        </>
      )}
    </main>
  )
}
