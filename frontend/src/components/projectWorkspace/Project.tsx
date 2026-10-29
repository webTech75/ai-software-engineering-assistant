import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'

import {
  sendChatMessageRequest,
  getChatHistoryRequest,
  getProjectRequest
} from '@/api/requests'

import { useAuth } from '@/components/auth/AuthContext'

import { ProjectHeader } from '@/components/projectWorkspace/ProjectHeader'
import { NeuraChat } from '@/components/projectWorkspace/chat/NeuraChat'
import type { Project } from '@/types/project'
import type { ChatMessage } from '@/types/chat'
import { ProjectSidebar } from '@/components/projectWorkspace/ProjectSidebar'
import { ProjectAnalysis } from './ProjectAnalysis'
import type { UploadResponse } from '@/types/chat'



export function Project() {
  const { projectId } = useParams<{ projectId: string }>()
  const id = Number(projectId)

  const { user, showToast } = useAuth()

  const [project, setProject] = useState<Project | null>(null)
  const [loadingProject, setLoadingProject] = useState(true)
  const [loading, setLoading] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(true)

  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([])

  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    loadProject()
    loadChatHistory()
  }, [projectId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth'
    })
  }, [messages])

  async function loadProject() {
    if (!projectId) {
      setLoadingProject(false)
      return
    }

    try {
      const data = await getProjectRequest(Number(projectId))

      setProject(data)
    } catch (error) {
      console.error('Unable to load project.', error)
      showToast('Unable to load project.', 'error')
    } finally {
      setLoadingProject(false)
    }
  }

  async function loadChatHistory() {
    if (!projectId) {
      setLoadingHistory(false)
      return
    }

    try {
      const history = await getChatHistoryRequest(Number(projectId))

      setMessages(history)
    } catch (error) {
      console.error('Unable to load chat history.', error)
      showToast('Unable to load chat history.', 'error')
    } finally {
      setLoadingHistory(false)
    }
  }

  // @ts-ignore
  async function handleSubmit(event) {
    event.preventDefault()

    const text = message.trim()

    if (!text || !projectId || !Number.isInteger(id) || id <= 0) {
      showToast('Enter a message and open a valid project.', 'error')
      return
    }

    setMessage('')

    setMessages(current => [
      ...current,
      {
        role: 'user',
        content: text
      }
    ])

    setLoading(true)

    try {
      const response = await sendChatMessageRequest(id, text)

      setMessages(current => [
        ...current,
        {
          role: 'assistant',
          content: response.answer
        }
      ])
    } catch (error) {
      console.error('Unable to get a response.', error)
      showToast('Unable to get a response. Please try again.', 'error')
      setMessage(text)
    } finally {
      setLoading(false)
    }
  }

  function handleProjectUpload(response: UploadResponse) {
    console.log("UPLOAD RESPONSE:", response)
    if (response.welcome) {

      setMessages(current => [
        ...current,
        {
          role: 'assistant',
          content: response.welcome?.message ?? ''
        }
      ])

    }
  }
  return (
    <div className='w-full space-y-8 px-6 py-6 lg:px-8'>
      {loadingProject ? (
        <p className='text-muted-foreground'>Loading project...</p>
      ) : project ? (
        <>
          <ProjectHeader project={project} />
          <ProjectAnalysis
            projectId={id}
            hasProjectFiles={Boolean(project.project_directory)}
          />
          <div className='mt-6 flex w-full min-w-0 rounded-xl border'>
            <ProjectSidebar projectId={id} onUploadSuccess={handleProjectUpload} />

            <div className='min-w-0 flex-1 p-6'>
              <NeuraChat
                messages={messages}
                message={message}
                loading={loading}
                loadingHistory={loadingHistory}
                username={user?.username}
                setMessage={setMessage}
                handleSubmit={handleSubmit}
                messagesEndRef={messagesEndRef}
              />
            </div>
          </div>
        </>
      ) : (
        <p className='text-destructive'>Project not found.</p>
      )}
    </div>
  )
}
