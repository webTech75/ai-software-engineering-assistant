import axios from 'axios'

import { storage, logout } from '@/components/auth/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
  //timeout: 60000
})

api.interceptors.request.use(
  config => {
    const token = storage.getToken()

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => {
    return response
  },

  error => {
    if (error.response?.status === 401) {
      logout()

      window.location.href = '/'
    }

    return Promise.reject(error)
  }
)

export { api }
