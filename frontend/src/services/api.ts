// TODO: Setup API client for making HTTP requests to backend
// Reference: https://axios-http.com/docs/intro

// import axios from 'axios'

// TODO: Create axios instance with base configuration
// const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
// const api = axios.create({
//   baseURL: API_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// })

// TODO: Define TypeScript interfaces for API responses
// These should match the Pydantic models from backend

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

// TODO: Implement API functions for each resource
// Group related endpoints together

// export const projectsApi = {
//   // TODO: GET /api/projects - List all projects
//   list: () => api.get<Project[]>('/api/projects'),
//   
//   // TODO: GET /api/projects/{id} - Get project by ID
//   get: (id: string) => api.get<Project>(`/api/projects/${id}`),
//   
//   // TODO: POST /api/projects - Create new project
//   create: (data: { name: string; path: string; description?: string }) =>
//     api.post<Project>('/api/projects', data),
//   
//   // TODO: DELETE /api/projects/{id} - Delete project
//   delete: (id: string) => api.delete(`/api/projects/${id}`),
//   
//   // TODO: POST /api/projects/{id}/index - Start indexing
//   index: (id: string) => api.post(`/api/projects/${id}/index`),
// }

// export const searchApi = {
//   // TODO: POST /api/search - Semantic search
//   search: (data: { project_id: string; query: string; top_k?: number }) =>
//     api.post<{ query: string; results: SearchResult[]; total: number }>('/api/search', data),
// }

// export const plansApi = {
//   // TODO: POST /api/plans/generate - Generate implementation plan
//   generate: (data: { project_id: string; task: string }) =>
//     api.post<Plan>('/api/plans/generate', data),
//   
//   // TODO: GET /api/plans/{id} - Get plan by ID
//   get: (id: string) => api.get<Plan>(`/api/plans/${id}`),
//   
//   // TODO: GET /api/plans/project/{projectId} - List plans for project
//   listByProject: (projectId: string) =>
//     api.get<Plan[]>(`/api/plans/project/${projectId}`),
// }

// export default api
