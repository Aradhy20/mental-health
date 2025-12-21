import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

// Service URLs for microservices architecture
const SERVICE_URLS = {
  auth: 'http://localhost:8001',
  text: 'http://localhost:8002',
  voice: 'http://localhost:8003',
  face: 'http://localhost:8004',
  fusion: 'http://localhost:8005',
  doctor: 'http://localhost:8006',
  notification: 'http://localhost:8007',
  moodJournal: 'http://localhost:8008',
  report: 'http://localhost:8009',
}

class ApiClient {
  private authClient: AxiosInstance
  private textClient: AxiosInstance
  private voiceClient: AxiosInstance
  private faceClient: AxiosInstance
  private fusionClient: AxiosInstance
  private doctorClient: AxiosInstance
  private notificationClient: AxiosInstance
  private moodJournalClient: AxiosInstance
  private reportClient: AxiosInstance

  constructor() {
    this.authClient = this.createClient(SERVICE_URLS.auth)
    this.textClient = this.createClient(SERVICE_URLS.text)
    this.voiceClient = this.createClient(SERVICE_URLS.voice)
    this.faceClient = this.createClient(SERVICE_URLS.face)
    this.fusionClient = this.createClient(SERVICE_URLS.fusion)
    this.doctorClient = this.createClient(SERVICE_URLS.doctor)
    this.notificationClient = this.createClient(SERVICE_URLS.notification)
    this.moodJournalClient = this.createClient(SERVICE_URLS.moodJournal)
    this.reportClient = this.createClient(SERVICE_URLS.report)
  }

  private createClient(baseURL: string): AxiosInstance {
    const client = axios.create({
      baseURL,
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' },
    })

    client.interceptors.request.use(
      (config: any) => {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          if (typeof window !== 'undefined') {
            localStorage.removeItem('token')
            window.location.href = '/login'
          }
        }
        return Promise.reject(error)
      }
    )

    return client
  }

  // Auth
  async login(username: string, password: string) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    const response = await this.authClient.post('/v1/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    return response.data
  }

  async register(userData: any) {
    const response = await this.authClient.post('/v1/register', userData)
    return response.data
  }

  async getCurrentUser() {
    const response = await this.authClient.get('/v1/users/me')
    return response.data
  }

  // Text Analysis
  async analyzeText(text: string, userId: string) {
    const response = await this.textClient.post('/v1/analyze/text', { text, user_id: userId })
    return response.data
  }

  async analyzeTextContextual(text: string, userId: string) {
    const response = await this.textClient.post('/v1/analyze/text/contextual', { text, user_id: userId })
    return response.data
  }

  async getEmotionHistory(userId: string, days: number = 30) {
    const response = await this.textClient.get(`/v1/analyze/emotion/history?user_id=${userId}&days=${days}`)
    return response.data
  }

  // Face Analysis
  async analyzeFace(userId: string, image: string) {
    const response = await this.faceClient.post('/v1/analyze/face', { user_id: userId, image })
    return response.data
  }

  // Mood & Journal
  async logMood(userId: string, moodLabel: string, score: number, notes?: string) {
    const response = await this.moodJournalClient.post('/v1/mood', {
      user_id: userId,
      mood_label: moodLabel,
      score,
      notes
    })
    return response.data
  }

  async getMoodHistory(userId: string, days: number = 30) {
    const response = await this.moodJournalClient.get(`/v1/mood/history/${userId}?days=${days}`)
    return response.data
  }

  async getMoodTrends(userId: string, days: number = 30) {
    const response = await this.moodJournalClient.get(`/v1/mood/trends/${userId}?days=${days}`)
    return response.data
  }

  async createJournalEntry(userId: string, title: string, content: string, mood?: string, tags?: string[]) {
    const response = await this.moodJournalClient.post('/v1/journal', {
      user_id: userId,
      title,
      content,
      mood,
      tags
    })
    return response.data
  }

  async getJournalEntries(userId: string, limit: number = 50, skip: number = 0) {
    const response = await this.moodJournalClient.get(`/v1/journal/${userId}?limit=${limit}&skip=${skip}`)
    return response.data
  }

  async updateJournalEntry(entryId: string, updates: any) {
    const response = await this.moodJournalClient.put(`/v1/journal/${entryId}`, updates)
    return response.data
  }

  async deleteJournalEntry(entryId: string) {
    const response = await this.moodJournalClient.delete(`/v1/journal/${entryId}`)
    return response.data
  }

  // Doctor Service
  async getNearbyDoctors(lat: number, lng: number, maxDistance: number = 50) {
    const response = await this.doctorClient.get(`/v1/doctor/nearby?lat=${lat}&lng=${lng}&max_distance=${maxDistance}`)
    return response.data
  }

  async getSpecialistDoctors(specialization: string, lat?: number, lng?: number) {
    let url = `/v1/doctor/specialists?specialization=${specialization}`
    if (lat && lng) {
      url += `&lat=${lat}&lng=${lng}`
    }
    const response = await this.doctorClient.get(url)
    return response.data
  }

  async getUserMedications(userId: string) {
    const response = await this.doctorClient.get(`/v1/medications/user/${userId}`)
    return response.data
  }

  async addMedication(medicationData: any) {
    const response = await this.doctorClient.post('/v1/medications', medicationData)
    return response.data
  }

  async updateMedication(medId: string, updates: any) {
    const response = await this.doctorClient.put(`/v1/medications/${medId}`, updates)
    return response.data
  }

  async deleteMedication(medId: string) {
    const response = await this.doctorClient.delete(`/v1/medications/${medId}`)
    return response.data
  }

  // Notification Service
  async getUserNotifications(userId: string) {
    const response = await this.notificationClient.get(`/v1/notifications/user/${userId}`)
    return response.data
  }

  async markNotificationRead(notifId: string) {
    const response = await this.notificationClient.put(`/v1/notifications/${notifId}`, { status: 'read' })
    return response.data
  }

  // Report Service
  async getUserReports(userId: string) {
    const response = await this.reportClient.get(`/v1/reports/user/${userId}`)
    return response.data
  }

  async generateReport(reportData: any) {
    const response = await this.reportClient.post('/v1/reports/generate', reportData)
    return response.data
  }

  // Generic methods
  get<T>(url: string, config?: AxiosRequestConfig) {
    return this.textClient.get<T>(url, config)
  }

  post<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.textClient.post<T>(url, data, config)
  }
}

export default new ApiClient()