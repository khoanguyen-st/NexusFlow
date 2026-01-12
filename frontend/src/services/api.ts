import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface Project {
  id: string
  name: string
  path: string
  description: string | null
  status: string
  file_count: number
  indexed_at: string | null
  created_at: string
  updated_at: string
}

export interface SearchResult {
  file_path: string
  file_name: string
  content: string
  similarity: number
}

export interface AffectedFile {
  path: string
  action: string
}

export interface ImplementationStep {
  order: number
  description: string
  file: string | null
}

export interface ReusableComponent {
  name: string
  location: string
  description: string | null
}

export interface Plan {
  id: string
  project_id: string
  task_description: string
  plan: {
    summary: string
    affected_files: AffectedFile[]
    steps: ImplementationStep[]
    reusable_components: ReusableComponent[]
  }
  context_used: string[]
  confidence: number
  created_at: string
}

// API Functions
export const projectsApi = {
  list: () => api.get<Project[]>('/api/projects'),
  get: (id: string) => api.get<Project>(`/api/projects/${id}`),
  create: (data: { name: string; path: string; description?: string }) =>
    api.post<Project>('/api/projects', data),
  delete: (id: string) => api.delete(`/api/projects/${id}`),
  index: (id: string) => api.post(`/api/projects/${id}/index`),
}

export const searchApi = {
  search: (data: { project_id: string; query: string; top_k?: number }) =>
    api.post<{ query: string; results: SearchResult[]; total: number }>('/api/search', data),
}

export const plansApi = {
  generate: (data: { project_id: string; task: string }) =>
    api.post<Plan>('/api/plans/generate', data),
  get: (id: string) => api.get<Plan>(`/api/plans/${id}`),
  listByProject: (projectId: string) =>
    api.get<Plan[]>(`/api/plans/project/${projectId}`),
}

export default api
