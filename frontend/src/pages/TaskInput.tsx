import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Sparkles, Loader2 } from 'lucide-react'
import { projectsApi, plansApi, Project } from '../services/api'

export default function TaskInput() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const [project, setProject] = useState<Project | null>(null)
  const [task, setTask] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (projectId) {
      loadProject(projectId)
    }
  }, [projectId])

  const loadProject = async (id: string) => {
    try {
      const response = await projectsApi.get(id)
      setProject(response.data)
    } catch (error) {
      console.error('Failed to load project:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!projectId || task.length < 10) return

    setLoading(true)
    setError('')

    try {
      const response = await plansApi.generate({
        project_id: projectId,
        task: task,
      })
      navigate(`/plan/${response.data.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate plan')
      setLoading(false)
    }
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Projects
        </button>
        <h1 className="text-3xl font-bold text-white">Generate Implementation Plan</h1>
        {project && (
          <p className="text-slate-400 mt-1">
            Project: <span className="text-sky-400">{project.name}</span>
          </p>
        )}
      </div>

      {/* Task Input Form */}
      <form onSubmit={handleSubmit} className="max-w-3xl">
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <label className="block text-lg font-medium text-white mb-4">
            Describe your task
          </label>
          <textarea
            value={task}
            onChange={(e) => setTask(e.target.value)}
            rows={6}
            className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-500 resize-none"
            placeholder="Example: Add a forgot password feature that sends a reset link to the user's email. The reset link should expire after 1 hour..."
            required
            minLength={10}
          />
          <p className="text-sm text-slate-500 mt-2">
            Be specific about what you want to implement. Include details about expected behavior, edge cases, and any constraints.
          </p>

          {error && (
            <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || task.length < 10}
            className="mt-6 flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating Plan...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Generate Plan
              </>
            )}
          </button>
        </div>

        {/* Tips */}
        <div className="mt-8 bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-4">Tips for better plans</h2>
          <ul className="space-y-2 text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-sky-400">•</span>
              Be specific about the feature you want to implement
            </li>
            <li className="flex items-start gap-2">
              <span className="text-sky-400">•</span>
              Mention any existing components or patterns you want to follow
            </li>
            <li className="flex items-start gap-2">
              <span className="text-sky-400">•</span>
              Include edge cases and error handling requirements
            </li>
            <li className="flex items-start gap-2">
              <span className="text-sky-400">•</span>
              Specify any third-party libraries you want to use
            </li>
          </ul>
        </div>
      </form>
    </div>
  )
}
