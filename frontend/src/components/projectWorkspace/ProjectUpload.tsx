import { Upload } from 'lucide-react'

import { uploadProjectRequest } from '@/api/requests'
import { useAuth } from '../auth/AuthContext'
import type { UploadResponse } from '@/types/chat'

interface ProjectUploadProps {
  projectId: number
  onSuccess: (response: UploadResponse) => void
}

export default function ProjectUpload ({
  projectId,
  onSuccess
}: ProjectUploadProps) {
  const { showLoader, hideLoader, showToast } = useAuth()

  async function handleUpload (event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]

    if (!file || !file.name.endsWith('.zip')) {
      showToast('Only ZIP files are supported.', 'error')
      return
    }

    try {
      showLoader('Uploading in progress...')
      const response = await uploadProjectRequest(projectId, file)

      onSuccess(response)
      showToast('Project uploaded successfully.', 'success')
    } catch (error: any) {
      console.log('Upload failed:', error)
      showToast('Upload failed. Please try again.', 'error')
    } finally {
      hideLoader()
    }
  }

  return (
    <div className='space-y-2'>
      <label className='flex cursor-pointer items-center gap-2 rounded-md border px-3 py-2 text-sm hover:bg-muted'>
        <Upload className='h-5 w-5 text-primary' />
        Upload Project
        <input type='file' accept='.zip' hidden onChange={handleUpload} />
      </label>
    </div>
  )
}
