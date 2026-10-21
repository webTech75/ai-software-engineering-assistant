import { useState } from 'react'

import { createProjectRequest } from '@/api/requests'
import type { Project } from '@/types/project'
import { useAuth } from '../auth/AuthContext'

interface CreateProjectFormProps {
  onCreated: (project: Project) => void
}

export function CreateProjectForm ({ onCreated }: CreateProjectFormProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [creating, setCreating] = useState(false)
  const { showLoader, hideLoader, showToast } = useAuth()

  // @ts-ignore
  async function handleSubmit (event) {
    event.preventDefault()

    if (!name.trim()) {
      showToast('Project name is required.', 'error')
      return
    }
    if (!description.trim()) {
      showToast('Project description is required.', 'error')
      return
    }

    try {
      setCreating(true)
      showLoader('Creating project...')

      const project = await createProjectRequest({
        name: name.trim(),
        description: description.trim() || undefined
      })

      onCreated(project)

      setName('')
      setDescription('')

      showToast('Project created successfully.', 'success')
    } catch {
      showToast('Unable to create project. Please try again.', 'error')
    } finally {
      setCreating(false)
      hideLoader()
    }
  }

  return (
    <section className='rounded-xl border p-6 shadow-sm'>
      <h2 className='mb-4 text-xl font-semibold'>Create a project</h2>

      <form onSubmit={handleSubmit} className='space-y-4'>
        <div className='space-y-2'>
          <label htmlFor='project-name' className='block text-sm font-medium'>
            Project name
          </label>

          <input
            id='project-name'
            type='text'
            value={name}
            onChange={event => {
              setName(event.target.value)
            }}
            placeholder='My software project'
            required
            className='w-full rounded-lg border bg-background p-3 text-foreground'
          />
        </div>

        <div className='space-y-2'>
          <label
            htmlFor='project-description'
            className='block text-sm font-medium'
          >
            Description
          </label>

          <textarea
            id='project-description'
            value={description}
            onChange={event => {
              setDescription(event.target.value)
            }}
            placeholder='Describe what you want to build...'
            rows={4}
            className='w-full rounded-lg border bg-background p-3 text-foreground'
          />
        </div>

        <button
          type='submit'
          disabled={creating || !name.trim() || !description.trim()}
          className='
            rounded-lg
            bg-primary
            px-5
            py-2
            text-primary-foreground
            hover:opacity-90
            disabled:cursor-not-allowed
            disabled:opacity-50
          '
        >
          {creating ? 'Creating...' : 'Create project'}
        </button>
      </form>
    </section>
  )
}
