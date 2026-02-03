import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Loader2,
  ArrowLeft,
  FilePlus,
  FileEdit,
  FileX,
  CheckCircle2,
  Circle,
  Package,
  Gauge,
} from "lucide-react";
import { plansApi, Plan } from "../services/api";

export default function PlanView() {
  const { planId } = useParams<{ planId: string }>();
  const navigate = useNavigate();
  const [plan, setPlan] = useState<Plan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [checkedSteps, setCheckedSteps] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (planId) {
      loadPlan(planId);
    }
  }, [planId]);

  const loadPlan = async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await plansApi.get(id);
      setPlan(response.data);
    } catch (err) {
      setError("Failed to load plan. Please try again.");
      console.error("Error loading plan:", err);
    } finally {
      setLoading(false);
    }
  };

  const toggleStep = (order: number) => {
    setCheckedSteps((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(order)) {
        newSet.delete(order);
      } else {
        newSet.add(order);
      }
      return newSet;
    });
  };

  const getActionBadge = (action: string) => {
    switch (action.toLowerCase()) {
      case "create":
        return {
          icon: FilePlus,
          color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
          label: "Create",
        };
      case "modify":
        return {
          icon: FileEdit,
          color: "bg-amber-500/20 text-amber-400 border-amber-500/30",
          label: "Modify",
        };
      case "delete":
        return {
          icon: FileX,
          color: "bg-red-500/20 text-red-400 border-red-500/30",
          label: "Delete",
        };
      default:
        return {
          icon: FileEdit,
          color: "bg-slate-500/20 text-slate-400 border-slate-500/30",
          label: action,
        };
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "text-emerald-400";
    if (confidence >= 0.6) return "text-amber-400";
    return "text-red-400";
  };

  const getConfidenceBarColor = (confidence: number) => {
    if (confidence >= 0.8) return "bg-emerald-500";
    if (confidence >= 0.6) return "bg-amber-500";
    return "bg-red-500";
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      </div>
    );
  }

  if (error || !plan) {
    return (
      <div className="text-center py-16">
        <p className="text-red-400 mb-4">{error || "Plan not found"}</p>
        <button
          onClick={() => navigate(-1)}
          className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Back Button */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(`/task/${plan.project_id}`)}
          className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5 text-slate-400" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-white">Implementation Plan</h1>
          <p className="text-sm text-slate-400">
            Created {new Date(plan.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      {/* Plan Summary */}
      <div className="bg-gradient-to-r from-sky-500/10 to-purple-500/10 border border-sky-500/20 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-2">Summary</h2>
        <p className="text-slate-300 leading-relaxed">{plan.plan.summary}</p>
      </div>

      {/* Confidence Score */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <Gauge className="w-5 h-5 text-sky-400" />
          <h2 className="text-lg font-semibold text-white">Confidence Score</h2>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex-1 h-3 bg-slate-700 rounded-full overflow-hidden">
            <div
              className={`h-full ${getConfidenceBarColor(plan.confidence)} transition-all duration-500`}
              style={{ width: `${plan.confidence * 100}%` }}
            />
          </div>
          <span className={`text-2xl font-bold ${getConfidenceColor(plan.confidence)}`}>
            {Math.round(plan.confidence * 100)}%
          </span>
        </div>
        <p className="text-sm text-slate-400 mt-2">
          {plan.confidence >= 0.8
            ? "High confidence - This plan is well-supported by the codebase analysis."
            : plan.confidence >= 0.6
            ? "Medium confidence - Some assumptions may need verification."
            : "Low confidence - Please review carefully before implementation."}
        </p>
      </div>

      {/* Affected Files */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-4">
          Affected Files ({plan.plan.affected_files.length})
        </h2>
        <div className="space-y-2">
          {plan.plan.affected_files.map((file, index) => {
            const badge = getActionBadge(file.action);
            const Icon = badge.icon;
            return (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg"
              >
                <code className="text-sm text-slate-300 font-mono">
                  {file.path}
                </code>
                <span
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-full border ${badge.color}`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  {badge.label}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Implementation Steps */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-4">
          Implementation Steps ({checkedSteps.size}/{plan.plan.steps.length} completed)
        </h2>
        <div className="space-y-3">
          {plan.plan.steps.map((step) => (
            <div
              key={step.order}
              onClick={() => toggleStep(step.order)}
              className={`flex items-start gap-3 p-4 rounded-lg cursor-pointer transition-all ${
                checkedSteps.has(step.order)
                  ? "bg-emerald-500/10 border border-emerald-500/20"
                  : "bg-slate-900/50 hover:bg-slate-900/80"
              }`}
            >
              <div className="mt-0.5">
                {checkedSteps.has(step.order) ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                ) : (
                  <Circle className="w-5 h-5 text-slate-500" />
                )}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-sky-400 font-semibold">
                    Step {step.order}
                  </span>
                  {step.file && (
                    <code className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
                      {step.file}
                    </code>
                  )}
                </div>
                <p
                  className={`mt-1 ${
                    checkedSteps.has(step.order)
                      ? "text-slate-400 line-through"
                      : "text-slate-300"
                  }`}
                >
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Reusable Components */}
      {plan.plan.reusable_components.length > 0 && (
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Package className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold text-white">
              Reusable Components ({plan.plan.reusable_components.length})
            </h2>
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {plan.plan.reusable_components.map((component, index) => (
              <div
                key={index}
                className="p-4 bg-slate-900/50 rounded-lg border border-purple-500/10"
              >
                <h3 className="font-medium text-purple-300">{component.name}</h3>
                <code className="text-xs text-slate-500 font-mono">
                  {component.location}
                </code>
                {component.description && (
                  <p className="text-sm text-slate-400 mt-2">
                    {component.description}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Task Description */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-2">Original Task</h2>
        <p className="text-slate-400">{plan.task_description}</p>
      </div>
    </div>
  );
}
