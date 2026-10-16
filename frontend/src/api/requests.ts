import { api } from './axios'

export async function getProjectsRequest () {
  const { data } = await api.get('/projects')
  return data
}

export async function getProjectRequest (projectId: number) {
  const { data } = await api.get(`/projects/${projectId}`)
  return data
}

export async function createProjectRequest (project: {
  name: string
  description?: string
}) {
  const { data } = await api.post('/projects', project)
  return data
}

export async function deleteProjectRequest (projectId: number) {
  const { data } = await api.delete(`/projects/${projectId}`)
  return data
}

// AI chat
export async function sendChatMessageRequest (
  projectId: number,
  message: string
) {
  const { data } = await api.post(`/chat/${projectId}`, {
    message
  })
  return data
}

// AI chat history
export async function getChatHistoryRequest (projectId: number) {
  const { data } = await api.get(`/chat/${projectId}/history`)
  return data
}

// Project files
export async function getProjectFilesRequest (projectId: number) {
  const { data } = await api.get(`/projects/${projectId}/files`)
  return data
}

export async function scanProjectRequest (projectId: number) {
  const { data } = await api.get(`/projects/${projectId}/scan`)
  return data
}
