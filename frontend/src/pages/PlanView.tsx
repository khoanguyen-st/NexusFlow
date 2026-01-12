import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, FileCode, GitBranch, Puzzle, Loader2 } from 'lucide-react'
import { plansApi, Plan } from '../services/api'

export default function PlanView() {
  const { planId } = useParams<{ planId: string }>()
  const navigate = useNavigate()
  const [plan, setPlan] = useState<Plan | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (planId) {
      loadPlan(planId)
    }
  }, [planId])

  const loadPlan = async (id: string) => {
    try {
      const response = await plansApi.get(id)
      setPlan(response.data)
    } catch (error) {
      console.error('Failed to load plan:', error)
    } finally {
      setLoading(false)
    }
  }

  const getActionBadge = (action: string) => {
    const styles: Record<string, string> = {
      create: 'bg-green-500/20 text-green-400',
      modify: 'bg-yellow-500/20 text-yellow-400',
      delete: 'bg-red-500/20 text-red-400',
    }
    return styles[action] || styles.modify
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      </div>
    )
  }

  if (!plan) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-400">Plan not found</p>
      </div>
    )
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
        <h1 className="text-3xl font-bold text-white">Implementation Plan</h1>
        <div className="flex items-center gap-4 mt-2">
          <span className="text-slate-400">
            Confidence: <span className="text-sky-400 font-medium">{Math.round(plan.confidence * 100)}%</span>
          </span>
          <span className="text-slate-500">
            Generated: {new Date(plan.created_at).toLocaleString()}
          </span>
        </div>
      </div>

      {/* Task Description */}
      <div className="bg-slate-800 rounded-xl p-6 mb-6 border border-slate-700">
        <h2 className="text-lg font-semibold text-white mb-3">Task</h2>
        <p className="text-slate-300">{plan.task_description}</p>
      </div>

      {/* Summary */}
      <div className="bg-gradient-to-r from-sky-500/10 to-blue-500/10 rounded-xl p-6 mb-6 border border-sky-500/30">
        <h2 className="text-lg font-semibold text-white mb-3">Summary</h2>
        <p className="text-slate-300">{plan.plan.summary}</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Affected Files */}
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <FileCode className="w-5 h-5 text-sky-400" />
            <h2 className="text-lg font-semibold text-white">Affected Files</h2>
          </div>
          <ul className="space-y-2">
            {plan.plan.affected_files.map((file, index) => (
              <li key={index} className="flex items-center gap-3 p-3 bg-slate-900 rounded-lg">
                <span className={`px-2 py-1 text-xs font-medium rounded ${getActionBadge(file.action)}`}>
                  {file.action}
                </span>
                <code className="text-sm text-slate-300 font-mono">{file.path}</code>
              </li>
            ))}
          </ul>
        </div>

        {/* Reusable Components */}
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-4">
            <Puzzle className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold text-white">Reusable Components</h2>
          </div>
          {plan.plan.reusable_components.length > 0 ? (
            <ul className="space-y-3">
              {plan.plan.reusable_components.map((component, index) => (
                <li key={index} className="p-3 bg-slate-900 rounded-lg">
                  <code className="text-sm text-purple-400 font-mono">{component.name}</code>
                  <p className="text-sm text-slate-500 mt-1">{component.location}</p>
                  {component.description && (
                    <p className="text-sm text-slate-400 mt-1">{component.description}</p>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-500">No reusable components identified</p>
          )}
        </div>
      </div>

      {/* Implementation Steps */}
      <div className="mt-6 bg-slate-800 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-2 mb-4">
          <GitBranch className="w-5 h-5 text-green-400" />
          <h2 className="text-lg font-semibold text-white">Implementation Steps</h2>
        </div>
        <ol className="space-y-4">
          {plan.plan.steps.map((step) => (
            <li key={step.order} className="flex gap-4 p-4 bg-slate-900 rounded-lg">
              <div className="flex-shrink-0 w-8 h-8 bg-sky-500/20 text-sky-400 rounded-full flex items-center justify-center font-medium">
                {step.order}
              </div>
              <div className="flex-1">
                <p className="text-slate-300">{step.description}</p>
                {step.file && (
                  <code className="text-sm text-slate-500 font-mono mt-2 block">
                    📄 {step.file}
                  </code>
                )}
              </div>
            </li>
          ))}
        </ol>
      </div>

      {/* Context Used */}
      <div className="mt-6 bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h2 className="text-sm font-medium text-slate-400 mb-3">Context Files Used</h2>
        <div className="flex flex-wrap gap-2">
          {plan.context_used.map((file, index) => (
            <span key={index} className="px-3 py-1 bg-slate-700 text-slate-300 text-sm rounded-full font-mono">
              {file}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
