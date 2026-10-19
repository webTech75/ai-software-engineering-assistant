import { useState } from 'react'
import { LoginForm } from './LoginForm'
import { useAuth } from './AuthContext'
import { ForgotPassword } from './ForgotPassword'

type AuthMode = 'login' | 'register' | 'forgot'

export function AuthCard () {
  const [mode, setMode] = useState<AuthMode>('login')
  const { user } = useAuth()
  console.log('user>>>', user)
  return (
    <div className='relative flex min-h-screen items-center justify-center p-4'>
      <div className='auth-card relative z-10 w-full max-w-md rounded-2xl p-8'>
        <div className='mb-8 text-center'>
          <h1 className='bg-gradient-to-r from-primary to-chart-2 bg-clip-text text-3xl font-bold text-transparent'>
            {mode === 'login'
              ? 'AI Software Engineering Assistant'
              : mode === 'register'
              ? 'Create Your Account'
              : 'Forgot Password'}
          </h1>

          <p className='mt-2 text-sm text-muted-foreground'>
            {mode === 'login'
              ? 'Your AI Pair Programmer'
              : mode === 'register'
              ? 'Join your AI Pair Programmer'
              : 'Enter your email address to reset your password'}
          </p>
        </div>
        {mode !== 'forgot' && (
          <div className='mb-6 flex rounded-lg border border-border p-1'>
            <button
              type='button'
              onClick={() => setMode('login')}
              className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-all ${
                mode === 'login'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-muted'
              }`}
            >
              Sign In
            </button>

            <button
              type='button'
              onClick={() => setMode('register')}
              className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-all ${
                mode === 'register'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-muted'
              }`}
            >
              Register
            </button>
          </div>
        )}

        {mode === 'login' && (
          <>
            <LoginForm mode={mode} setMode={setMode} />

            <button
              type='button'
              onClick={() => setMode('forgot')}
              className='mt-4 w-full text-sm text-primary hover:underline'
            >
              Forgot Password?
            </button>
          </>
        )}

        {mode === 'register' && <LoginForm mode={mode} setMode={setMode} />}

        {mode === 'forgot' && (
          <div className='text-center text-sm text-muted-foreground'>
            <ForgotPassword onBack={() => setMode('login')} />
          </div>
        )}
      </div>
    </div>
  )
}
