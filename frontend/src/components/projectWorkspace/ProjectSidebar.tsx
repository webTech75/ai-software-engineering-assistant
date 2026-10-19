import { ProjectFiles } from '@/components/projectWorkspace/ProjectFiles'

interface ProjectSidebarProps {
  projectId: number
}

export function ProjectSidebar ({ projectId }: ProjectSidebarProps) {
  return (
    <aside className='flex h-[700px] w-72 flex-col border-r p-4'>
      <ProjectFiles projectId={projectId} />
    </aside>
  )
}
