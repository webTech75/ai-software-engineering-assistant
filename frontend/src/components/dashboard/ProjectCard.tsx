import { useNavigate } from 'react-router-dom'
import type { Project } from '@/types/project'
import { Trash2 } from 'lucide-react'
import { deleteProjectRequest } from '@/api/requests'
import { useAuth } from '../auth/AuthContext'

interface ProjectCardProps {
  project: Project
  onRefresh: () => Promise<void>
}

export function ProjectCard ({ project, onRefresh }: ProjectCardProps) {
  const navigate = useNavigate()
  const { confirm, showLoader, hideLoader, showToast } = useAuth()

  function confirmDelete () {
    confirm({
      title: 'Delete Project',
      description: `Are you sure you want to delete "${project.name}"? 
                      This will permanently remove the project, 
                      all related files, and chat history.`,
      confirmText: 'Delete',
      onConfirm: handleDeleteProject
    })
  }

  async function handleDeleteProject () {
    try {
      showLoader('Deleting project...')

      await deleteProjectRequest(project.id)
      await onRefresh()
      showToast('Project deleted successfully.', 'success')
    } catch (error) {
      showToast('Unable to delete project.', 'error')
    } finally {
      hideLoader()
    }
  }

  return (
    <article className='flex h-full flex-col rounded-xl border bg-card p-5 shadow-sm transition hover:shadow-md'>
      <h3 className='text-lg font-semibold'>{project.name}</h3>

      <p className='mt-3 line-clamp-4 text-sm text-muted-foreground'>
        {project.description || 'No description provided.'}
      </p>

      <p className='mt-4 text-xs text-muted-foreground'>
        Project ID: {project.id}
      </p>

      <div className='mt-auto flex items-center gap-2'>
        <button
          type='button'
          onClick={() => navigate(`/projects/${project.id}`)}
          className='
          flex-1
          rounded-lg
          bg-primary
          px-4
          py-2
          text-sm
          font-medium
          text-primary-foreground
          transition-opacity
          hover:opacity-90
        '
        >
          Open Workspace →
        </button>

        <button
          type='button'
          onClick={confirmDelete}
          className='
          rounded-lg
          border
          p-2
          text-muted-foreground
          transition-colors
          hover:border-destructive
          hover:bg-destructive/10
          hover:text-destructive
        '
          aria-label='Delete project'
        >
          <Trash2 className='h-4 w-4' />
        </button>
      </div>
    </article>
  )
}
