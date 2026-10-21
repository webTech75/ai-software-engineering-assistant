import { LandingHeader } from '@/components/landing/LandingHeader'
import { Hero } from '@/components/landing/Hero'
import { AuthBackground } from '@/components/common/AuthBackground'
import { useState } from 'react'
import { AuthCard } from '@/components/auth/AuthCard'
import { Navigate } from 'react-router-dom'
import { storage } from '@/components/auth/auth'
import { Footer } from '@/components/common/Footer'

export function Landing () {
  const [showLogin, setShowLogin] = useState(false)

  const token = storage.getToken()

  if (token) {
    return <Navigate to='/dashboard' replace />
  }

  return (
    <main className='relative min-h-screen bg-background'>
      <AuthBackground />

      <div className='relative z-10'>
        {showLogin ? (
          <AuthCard />
        ) : (
          <>
            <LandingHeader onLogin={() => setShowLogin(true)} />
            <Hero />
            <Footer />
          </>
        )}
      </div>
    </main>
  )
}
