import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Folder, RefreshCw, Trash2, ArrowRight, Loader2 } from 'lucide-react'
import { projectsApi, Project } from '../services/api'

export default function Projects() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', path: '', description: '' })
  const [indexingId, setIndexingId] = useState<string | null>(null)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      const response = await projectsApi.list()
      setProjects(response.data)
    } catch (error) {
      console.error('Failed to load projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await projectsApi.create(formData)
      setFormData({ name: '', path: '', description: '' })
      setShowForm(false)
      loadProjects()
    } catch (error) {
      console.error('Failed to create project:', error)
    }
  }

  const handleIndex = async (id: string) => {
    setIndexingId(id)
    try {
      await projectsApi.index(id)
      // Poll for status updates
      const checkStatus = setInterval(async () => {
        const response = await projectsApi.get(id)
        if (response.data.status !== 'indexing') {
          clearInterval(checkStatus)
          setIndexingId(null)
          loadProjects()
        }
      }, 2000)
    } catch (error) {
      console.error('Failed to index project:', error)
      setIndexingId(null)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this project?')) return
    try {
      await projectsApi.delete(id)
      loadProjects()
    } catch (error) {
      console.error('Failed to delete project:', error)
    }
  }

  const getStatusBadge = (status: string) => {
    const styles: Record<string, string> = {
      pending: 'bg-yellow-500/20 text-yellow-400',
      indexing: 'bg-blue-500/20 text-blue-400',
      ready: 'bg-green-500/20 text-green-400',
      error: 'bg-red-500/20 text-red-400',
    }
    return styles[status] || styles.pending
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Projects</h1>
          <p className="text-slate-400 mt-1">Manage your codebases for AI analysis</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
          Add Project
        </button>
      </div>

      {/* Add Project Form */}
      {showForm && (
        <form onSubmit={handleCreate} className="bg-slate-800 rounded-xl p-6 mb-8 border border-slate-700">
          <h2 className="text-xl font-semibold mb-4">New Project</h2>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Project Name
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-sky-500"
                placeholder="My Project"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Project Path
              </label>
              <input
                type="text"
                value={formData.path}
                onChange={(e) => setFormData({ ...formData, path: e.target.value })}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-sky-500"
                placeholder="/projects/my-project"
                required
              />
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Description (optional)
            </label>
            <input
              type="text"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              placeholder="A brief description of the project"
            />
          </div>
          <div className="flex gap-3 mt-6">
            <button
              type="submit"
              className="px-4 py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-lg transition-colors"
            >
              Create Project
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Projects List */}
      {projects.length === 0 ? (
        <div className="text-center py-16 bg-slate-800/50 rounded-xl border border-slate-700">
          <Folder className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-slate-300 mb-2">No projects yet</h2>
          <p className="text-slate-500">Add a project to get started with AI analysis</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {projects.map((project) => (
            <div
              key={project.id}
              className="bg-slate-800 rounded-xl p-6 border border-slate-700 hover:border-slate-600 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold text-white">{project.name}</h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusBadge(project.status)}`}>
                      {project.status}
                    </span>
                  </div>
                  <p className="text-slate-400 text-sm font-mono mb-2">{project.path}</p>
                  {project.description && (
                    <p className="text-slate-500 text-sm">{project.description}</p>
                  )}
                  <div className="flex items-center gap-4 mt-3 text-sm text-slate-500">
                    <span>{project.file_count} files indexed</span>
                    {project.indexed_at && (
                      <span>Last indexed: {new Date(project.indexed_at).toLocaleDateString()}</span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleIndex(project.id)}
                    disabled={indexingId === project.id}
                    className="p-2 text-slate-400 hover:text-sky-400 hover:bg-slate-700 rounded-lg transition-colors disabled:opacity-50"
                    title="Re-index project"
                  >
                    <RefreshCw className={`w-5 h-5 ${indexingId === project.id ? 'animate-spin' : ''}`} />
                  </button>
                  <button
                    onClick={() => handleDelete(project.id)}
                    className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-700 rounded-lg transition-colors"
                    title="Delete project"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => navigate(`/task/${project.id}`)}
                    disabled={project.status !== 'ready'}
                    className="flex items-center gap-2 px-4 py-2 bg-sky-500/20 hover:bg-sky-500/30 text-sky-400 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Generate Plan
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
