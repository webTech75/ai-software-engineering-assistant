import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode
} from 'react'
import { logout as clearAuth, storage } from './auth'
import { getCurrentUserRequest } from '@/api/authReq'
import { toast } from 'sonner'
import type { ConfirmRequest, AuthContextType } from '@/types/project'
import ConfirmModal from '@/components/common/ConfirmModal'

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider ({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [loadingMessage, setLoadingMessage] = useState('')
  const [confirmRequest, setConfirmRequest] = useState<ConfirmRequest | null>(
    null
  )

  function confirm (request: ConfirmRequest) {
    setConfirmRequest(request)
  }

  async function refreshUser () {
    if (!storage.getToken()) {
      setUser(null)
      return
    }

    try {
      setUser(await getCurrentUserRequest())
    } catch {
      setUser(null)
      throw new Error('Failed to load user')
    }
  }

  useEffect(() => {
    refreshUser().catch(() => {})
  }, [])

  function logout () {
    clearAuth()
    setUser(null)
  }

  function showLoader (message?: string) {
    setLoadingMessage(message ?? 'Processing...')
    setLoading(true)
  }

  function hideLoader () {
    setLoading(false)
    setLoadingMessage('')
  }

  function showToast (
    message: string,
    type: 'success' | 'error' | 'info' = 'info'
  ) {
    switch (type) {
      case 'success':
        toast.success(message)
        break

      case 'error':
        toast.error(message)
        break

      default:
        toast.info(message)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        loadingMessage,
        confirm,
        showToast,
        refreshUser,
        logout,
        showLoader,
        hideLoader
      }}
    >
      <>
        {children}

        {confirmRequest && (
          <ConfirmModal
            open={true}
            title={confirmRequest.title}
            description={confirmRequest.description}
            confirmText={confirmRequest.confirmText}
            cancelText={confirmRequest.cancelText}
            onCancel={() => setConfirmRequest(null)}
            onConfirm={async () => {
              await confirmRequest.onConfirm()
              setConfirmRequest(null)
            }}
          />
        )}
      </>
    </AuthContext.Provider>
  )
}

export function useAuth () {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }

  return context
}
