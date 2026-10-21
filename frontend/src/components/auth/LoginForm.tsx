import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext'
import { registerRequest } from '@/api/authReq'

import { login } from './auth'

type AuthMode = 'login' | 'register' | 'forgot'

type LoginFormProps = {
  mode: AuthMode
  setMode: (mode: AuthMode) => void
}

export function LoginForm ({ mode, setMode }: LoginFormProps) {
  const navigate = useNavigate()
  const { refreshUser, showLoader, hideLoader, showToast, loading } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [email, setEmail] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [registrationCode, setRegistrationCode] = useState('')

  // @ts-ignore
  async function handleSubmit (event) {
    event.preventDefault()

    setError('')

    if (!username.trim()) {
      setError('Username is required.')
      return
    }
    if (username.length < 3) {
      setError('Username must be at least 3 characters.')
      return
    }

    if (!password.trim()) {
      setError('Password is required.')
      return
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }

    if (mode === 'register') {
      if (username.length < 3) {
        setError('Username must be at least 3 characters.')
        return
      }

      if (username.length > 30) {
        setError('Username cannot exceed 30 characters.')
        return
      }

      const usernameRegex = /^[A-Za-z][A-Za-z0-9_]*$/

      if (!usernameRegex.test(username)) {
        setError(
          'Username must start with a letter and contain only letters, numbers, and underscores.'
        )
        return
      }

      if (!email.trim()) {
        setError('Email is required.')
        return
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

      if (!emailRegex.test(email)) {
        setError('Please enter a valid email address.')
        return
      }

      if (password.length < 8) {
        setError('Password must be at least 8 characters long.')
        return
      }

      if (!confirmPassword.trim()) {
        setError('Please confirm your password.')
        return
      }

      if (password !== confirmPassword) {
        setError('Passwords do not match.')
        return
      }

      if (!registrationCode.trim()) {
        setError('Registration Code is required.')
        return
      }
    }

    if (mode === 'forgot') {
      return
    }

    try {
      showLoader()

      if (mode === 'login') {
        await login(username, password)
        await refreshUser()
        setUsername('')
        setPassword('')
        navigate('/dashboard', { replace: true })
      } else {
        await registerRequest({ username, email, password, registrationCode })
        showToast('Account created successfully. Please sign in.', 'success')
        setPassword('')
        setUsername('')
        setEmail('')
        setConfirmPassword('')
        setRegistrationCode('')
        setMode('login')
      }
    } catch (err: any) {
      console.log('login or create account error:', err)
      mode === 'login'
        ? showToast('Invalid username or password.', 'error')
        : showToast('Unable to create account.', 'error')
    } finally {
      hideLoader()
    }
  }

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className='space-y-4 transition-all duration-300'
      >
        <div>
          <label htmlFor='username' className='mb-2 block text-sm font-medium'>
            Username
          </label>
          <input
            id='username'
            type='text'
            autoComplete='username'
            value={username}
            onChange={e => {
              setUsername(e.target.value)
              setError('')
            }}
            className='w-full px-3 py-2 outline-none focus:border-primary'
          />
        </div>

        {mode === 'register' && (
          <div>
            <label htmlFor='email' className='mb-2 block text-sm font-medium'>
              Email
            </label>

            <input
              id='email'
              type='email'
              autoComplete='email'
              value={email}
              onChange={e => {
                setEmail(e.target.value)
                setError('')
              }}
              className='w-full px-3 py-2 outline-none focus:border-primary'
            />
          </div>
        )}
        <div>
          <label htmlFor='password' className='mb-2 block text-sm font-medium'>
            Password
          </label>
          <input
            id='password'
            type='password'
            autoComplete='current-password'
            value={password}
            onChange={e => {
              setPassword(e.target.value)
              setError('')
            }}
            className='w-full px-3 py-2 outline-none focus:border-primary'
          />
        </div>
        {mode === 'register' && (
          <>
            <div>
              <label
                htmlFor='confirmPassword'
                className='mb-2 block text-sm font-medium'
              >
                Confirm Password
              </label>

              <input
                id='confirmPassword'
                type='password'
                autoComplete='new-password'
                value={confirmPassword}
                onChange={e => {
                  setConfirmPassword(e.target.value)
                  setError('')
                }}
                className='w-full px-3 py-2 outline-none focus:border-primary'
              />
            </div>
            <div>
              <label
                htmlFor='registrationCode'
                className='mb-2 block text-sm font-medium'
              >
                Registration Code
              </label>
              <input
                id='registrationCode'
                type='password'
                value={registrationCode}
                onChange={e => {
                  setRegistrationCode(e.target.value)
                  setError('')
                }}
                className='w-full px-3 py-2 outline-none focus:border-primary'
              />
            </div>
          </>
        )}

        {error && <p className='text-sm text-red-500'>{error}</p>}

        <button
          type='submit'
          disabled={loading}
          className='btn-primary w-full py-2.5 font-medium disabled:opacity-50'
        >
          {loading
            ? mode === 'login'
              ? 'Signing In...'
              : 'Creating Account...'
            : mode === 'login'
            ? 'Sign In'
            : 'Create Account'}
        </button>
      </form>
    </>
  )
}
