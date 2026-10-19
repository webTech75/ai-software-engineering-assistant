import { Outlet } from 'react-router-dom'

import { Header } from '@/components/common/Header'
import NeuraLoader from '@/components/common/NeuraLoader'
import { useAuth } from '@/components/auth/AuthContext'

export function AppLayout () {
  const { loading, loadingMessage } = useAuth()

  return (
    <div className='flex h-screen flex-col'>
      <header className='fixed top-0 z-50 h-16 w-full border-b bg-background'>
        <Header />
      </header>

      <main className='flex-1 overflow-y-auto pt-16'>
        <Outlet />
      </main>
      <NeuraLoader show={loading} text={loadingMessage} />
    </div>
  )
}
