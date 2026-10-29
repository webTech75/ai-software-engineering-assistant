import { ProjectFiles } from '@/components/projectWorkspace/ProjectFiles'
import type { UploadResponse } from '@/types/chat'


interface ProjectSidebarProps {
  projectId: number
  onUploadSuccess: (response: UploadResponse) => void
}

export function ProjectSidebar ({ projectId, onUploadSuccess}: ProjectSidebarProps) {
  return (
    <aside className='flex h-[700px] w-72 flex-col border-r p-4'>
      <ProjectFiles projectId={projectId} onUploadSuccess={onUploadSuccess} />
    </aside>
  )
}
