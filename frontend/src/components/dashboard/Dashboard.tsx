import { useEffect, useState } from 'react'

import { getProjectsRequest } from '@/api/requests'

import { CreateProjectForm } from '@/components/dashboard/CreateProjectForm'
import { ProjectList } from '@/components/dashboard/ProjectList'
import type { Project } from '@/types/project'
import { useAuth } from '@/components/auth/AuthContext'
import { formatName } from '@/utils/formatName'

export function Dashboard () {
  const { user, showLoader, hideLoader, showToast } = useAuth()
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  async function loadProjects () {
    try {
      showLoader('Loading projects...')

      const projects = await getProjectsRequest()

      setProjects(projects)
    } catch {
      showToast('Unable to load projects. Please try again.', 'error')
    } finally {
      setLoading(false)
      hideLoader()
    }
  }

  useEffect(() => {
    loadProjects()
  }, [])

  return (
    <div className='mx-auto w-full max-w-6xl space-y-8'>
      <section className='text-center'>
        <img
          src='/neura_icon.png'
          alt='Neura'
          className='mx-auto h-24 w-24 rounded-2xl'
        />

        <h1 className='mt-6 text-4xl font-bold'>Neura</h1>

        <p className='mt-2 text-xl text-muted-foreground'>
          Your AI Software Engineering Assistant
        </p>

        <p className='mt-4 text-muted-foreground'>
          Welcome back, {formatName(user?.username)} 👋
        </p>

        <p className='mt-2 text-muted-foreground'>
          Manage your projects and AI engineering workspace.
        </p>
      </section>

      <CreateProjectForm
        onCreated={project => setProjects(current => [...current, project])}
      />

      <ProjectList
        projects={projects}
        loading={loading}
        onRefresh={loadProjects}
      />
    </div>
  )
}
