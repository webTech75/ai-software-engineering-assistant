import { useState } from 'react'
import { useAuth } from './AuthContext'
import { forgotPasswordRequest } from '@/api/authReq'

type ForgotPasswordProps = {
  onBack: () => void
}

export function ForgotPassword ({ onBack }: ForgotPasswordProps) {
  const { showLoader, hideLoader, showToast, loading } = useAuth()
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')

  // @ts-ignore
  async function handleSubmit (event) {
    event.preventDefault()

    if (error) setError('')

    if (!email.trim()) {
      setError('Email is required.')
      return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address.')
      return
    }

    try {
      showLoader()
      await forgotPasswordRequest(email)
      showToast(
        'If an account exists, a password reset link has been sent.',
        'info'
      )
      setEmail('')
      setEmail('')
    } catch (err) {
      console.error(err)
      showToast('Unable to process your request.', 'error')
    } finally {
      hideLoader()
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit} className='space-y-4'>
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

        {error && (
          <p className='text-sm text-destructive' role='alert'>
            {error}
          </p>
        )}

        <button
          type='submit'
          disabled={loading}
          className='btn-primary w-full py-2.5 font-medium disabled:opacity-50'
        >
          {loading ? 'Sending...' : 'Send Reset Link'}
        </button>

        <button
          type='button'
          onClick={onBack}
          className='w-full text-sm text-primary hover:underline'
        >
          Back to Sign In
        </button>
      </form>
    </>
  )
}
