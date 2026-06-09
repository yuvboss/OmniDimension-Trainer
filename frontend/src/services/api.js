import axios from 'axios'

const API_BASE = '/api'

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const industriesAPI = {
  getAll: () => apiClient.get('/industries'),
}

export const scenariosAPI = {
  getByIndustry: (industryId, difficulty = null) => {
    const params = difficulty ? { difficulty } : {}
    return apiClient.get(`/industries/${industryId}/scenarios`, { params })
  },
  getDetail: (scenarioId) => apiClient.get(`/scenarios/${scenarioId}`),
}

export const callsAPI = {
  start: (scenarioId, phoneNumber) =>
    apiClient.post('/calls/start', { scenario_id: scenarioId, phone_number: phoneNumber }),
  getStatus: (callId) => apiClient.get(`/calls/${callId}/status`),
  end: (callId) => apiClient.post(`/calls/${callId}/end`, {}),
}

export default apiClient
