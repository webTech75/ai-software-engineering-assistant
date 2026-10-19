import { ProjectCard } from './ProjectCard'
import type { Project } from '@/types/project'

interface ProjectListProps {
  projects: Project[]
  loading: boolean
  onRefresh: () => Promise<void>
}

export function ProjectList ({
  projects,
  loading,
  onRefresh
}: ProjectListProps) {
  return (
    <section className='rounded-xl border p-6 shadow-sm'>
      <div className='mb-4 flex items-center justify-between'>
        <h2 className='mb-4 text-xl font-semibold'>Your projects</h2>

        <button
          type='button'
          onClick={onRefresh}
          disabled={loading}
          className='
          mt-4
          rounded-lg
          border
          px-4
          py-2
          hover:bg-accent
          disabled:opacity-50
        '
        >
          Refresh projects
        </button>
      </div>
      {loading ? (
        <p>Loading projects...</p>
      ) : projects.length === 0 ? (
        <p className='text-muted-foreground'>
          You haven't created any projects yet.
        </p>
      ) : (
        <div className='grid gap-6 sm:grid-cols-2 lg:grid-cols-3'>
          {projects.map(project => (
            <ProjectCard
              key={project.id}
              onRefresh={onRefresh}
              project={project}
            />
          ))}
        </div>
      )}
    </section>
  )
}
