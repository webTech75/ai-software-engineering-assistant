import { X } from 'lucide-react'
import { useState } from 'react'
import type { ConfirmModalProps } from '@/types/project'

export default function ConfirmModal ({
  open,
  title,
  description,
  confirmText = 'Delete',
  cancelText = 'Cancel',
  onConfirm,
  onCancel
}: ConfirmModalProps) {
  if (!open) return null

  const [confirming, setConfirming] = useState(false)

  async function handleConfirm () {
    try {
      setConfirming(true)
      await onConfirm()
    } finally {
      setConfirming(false)
    }
  }

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/50'>
      <div className='w-full max-w-md rounded-xl border bg-background p-6 shadow-xl'>
        <div className='flex items-center justify-between'>
          <h2 className='text-lg font-semibold'>{title}</h2>

          <button
            type='button'
            onClick={onCancel}
            className='text-muted-foreground hover:text-foreground'
          >
            <X className='h-5 w-5' />
          </button>
        </div>

        <p className='mt-3 text-sm text-muted-foreground'>{description}</p>

        <div className='mt-6 flex justify-end gap-3'>
          <button
            type='button'
            onClick={onCancel}
            className='rounded-lg border px-4 py-2 text-sm'
          >
            {cancelText}
          </button>

          <button
            type='button'
            onClick={handleConfirm}
            disabled={confirming}
            className='rounded-lg bg-destructive px-4 py-2 text-sm text-destructive-foreground disabled:opacity-50'
          >
            {confirming ? 'Deleting...' : confirmText}
          </button>
        </div>
      </div>
    </div>
  )
}
