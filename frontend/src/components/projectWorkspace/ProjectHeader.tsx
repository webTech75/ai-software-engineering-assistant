import type { Project } from '@/types/project'
import { useNavigate } from 'react-router-dom'

interface ProjectHeaderProps {
  project: Project
}

export function ProjectHeader ({ project }: ProjectHeaderProps) {
  const navigate = useNavigate()
  return (
    <section>
      <div className='mb-4 flex items-center justify-between'>
        <h1 className='text-3xl font-bold'>Project Workspace</h1>

        <button
          type='button'
          onClick={() => navigate('/')}
          className='rounded-lg border bg-card px-3 py-1.5 text-sm transition-colors hover:bg-accent'
        >
          ← Dashboard
        </button>
      </div>
      <div className='mt-2 space-y-1'>
        <div className='flex items-center gap-3'>
          <p className='text-xl font-semibold'>{project.name}</p>

          <span className='text-sm text-muted-foreground'>
            -- Project ID: {project.id}
          </span>
        </div>

        {project.description && (
          <p className='text-muted-foreground'>{project.description}</p>
        )}
      </div>
    </section>
  )
}
