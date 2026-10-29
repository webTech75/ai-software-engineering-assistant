export interface Project {
  id: number
  name: string
  description?: string | null
  project_directory?: string | null
  owner_id?: number
  created_at?: string
}

// Modal
export interface ConfirmRequest {
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void | Promise<void>
}
export interface ConfirmModalProps {
  open: boolean
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void
  onCancel: () => void
}

// components/auth/authContext type
export interface AuthContextType {
  user: any
  loading: boolean
  loadingMessage: string
  confirm: (request: ConfirmRequest) => void
  showToast: (message: string, type?: 'success' | 'error' | 'info') => void
  refreshUser: () => Promise<void>
  logout: () => void
  showLoader: (message?: string) => void
  hideLoader: () => void
}
