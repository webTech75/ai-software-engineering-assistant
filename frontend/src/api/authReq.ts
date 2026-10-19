import { api } from './axios'

export async function registerRequest (user: {
  username: string
  email: string
  password: string
  registrationCode: string
}) {
  const { data } = await api.post('/users/register', {
    username: user.username.trim().toLowerCase(),
    email: user.email.trim().toLowerCase(),
    password: user.password,
    registration_code: user.registrationCode
  })

  return data
}

export async function forgotPasswordRequest (email: string) {
  const { data } = await api.post('/users/forgot-password', {
    email: email.trim().toLowerCase()
  })

  return data
}

export async function resetPasswordRequest (token: string, password: string) {
  const { data } = await api.post('/users/reset-password', {
    token,
    password
  })

  return data
}

export async function getCurrentUserRequest () {
  const { data } = await api.get('/users/me')

  return data
}

// login body expect URLSearchParams
export async function loginRequest (username: string, password: string) {
  const formData = new URLSearchParams()

  formData.append('username', username.trim().toLowerCase())
  formData.append('password', password)

  const { data } = await api.post('/users/login', formData)

  return data
}
