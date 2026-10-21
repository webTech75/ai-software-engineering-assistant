import { useNavigate } from 'react-router-dom'
import { LockOpen } from 'lucide-react'

import { useAuth } from '../auth/AuthContext'
import { Logo } from '@/components/common/Logo'
import { ThemeSwitcher } from '@/components/common/ThemeSwitcher'

export function Header () {
  const navigate = useNavigate()
  const { logout, user } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/', { replace: true })
  }

  return (
    <header className='flex h-16 items-center justify-between border-b px-6'>
      <Logo />

      <div className='flex items-center gap-2'>
        <ThemeSwitcher />
        {user && (
          <span className='text-sm font-semibold uppercase'>
            Hi, {user.username}
          </span>
        )}

        {/* <button
          type='button'
          className='rounded-lg p-2 transition-colors hover:bg-accent'
        >
          <User className='h-5 w-5' />
        </button> */}

        <button
          type='button'
          onClick={handleLogout}
          className='flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent'
        >
          <LockOpen className='h-5 w-5 text-green-500' />
          <span>Logout</span>
        </button>
      </div>
    </header>
  )
}
