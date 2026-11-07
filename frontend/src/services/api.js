import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export const authApi = {
  register: (payload) => api.post('/api/auth/register', payload),
  login: (payload) => api.post('/api/auth/login', payload),
  me: () => api.get('/api/auth/me'),
}

export const dashboardApi = {
  summary: () => api.get('/api/dashboard/summary'),
}

export const analysisApi = {
  text: (payload) => api.post('/api/analyses/text', payload),
  url: (payload) => api.post('/api/analyses/url', payload),
  qr: (formData) => api.post('/api/analyses/qr', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
}

export const historyApi = {
  list: (page = 1, pageSize = 10) => api.get(`/api/analyses/history?page=${page}&page_size=${pageSize}`),
  get: (id) => api.get(`/api/analyses/${id}`),
}

export const alertsApi = {
  list: () => api.get('/api/alerts'),
  markRead: (id) => api.patch(`/api/alerts/${id}/read`),
}

export const profileApi = {
  get: () => api.get('/api/profile'),
  update: (payload) => api.put('/api/profile', payload),
  updatePassword: (payload) => api.put('/api/profile/password', payload),
  deleteAccount: (password) => api.delete('/api/profile', { data: { password } }),
}

export default api
