import { api } from './axios'

// =====================
// Projects
// =====================

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

// There an endpoint for it but not needed for now, may be in future.
export async function updateProjectRequest (
  projectId: number,
  project: {
    name: string
    description?: string
  }
) {
  const { data } = await api.put(`/projects/${projectId}`, project)

  return data
}

export async function deleteProjectRequest (projectId: number) {
  const { data } = await api.delete(`/projects/${projectId}`)

  return data
}

// =====================
// Project Upload
// =====================

export async function uploadProjectRequest (projectId: number, file: File) {
  const formData = new FormData()

  formData.append('file', file)

  const { data } = await api.post(`/projects/${projectId}/upload`, formData)

  return data
}

// =====================
// Project Analysis
// =====================

export async function scanProjectRequest (projectId: number) {
  const { data } = await api.get(`/projects/${projectId}/scan`)

  return data
}

export async function reindexProjectRequest (projectId: number) {
  const { data } = await api.post(`/projects/${projectId}/reindex`)

  return data
}

export async function getProjectIndexStatusRequest (projectId: number) {
  const { data } = await api.get(`/projects/${projectId}/index-status`)

  return data
}

// =====================
// Project Files
// =====================

export async function readProjectFileRequest (
  projectId: number,
  filePath: string
) {
  const { data } = await api.get(`/projects/${projectId}/file`, {
    params: {
      path: filePath
    }
  })

  return data
}

export async function searchProjectRequest (projectId: number, query: string) {
  const { data } = await api.get(`/projects/${projectId}/search`, {
    params: {
      query
    }
  })

  return data
}

// =====================
// AI Chat
// =====================

export async function sendChatMessageRequest (
  projectId: number,
  message: string
) {
  const { data } = await api.post(`/chat`, {
    message,
    project_id: projectId
  })

  return data
}

export async function getChatHistoryRequest (projectId: number) {
  const { data } = await api.get(`/chat/history?project_id=${projectId}`)

  return data
}
