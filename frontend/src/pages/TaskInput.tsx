import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Loader2, Sparkles, ChevronDown } from "lucide-react";
import { projectsApi, plansApi, Project } from "../services/api";

export default function TaskInput() {
  const navigate = useNavigate();

  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>("");
  const [task, setTask] = useState("");
  const [loading, setLoading] = useState(false);
  const [projectsLoading, setProjectsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const selectedProject = projects.find((p) => p.id === selectedProjectId);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await projectsApi.list();
      setProjects(response.data);

      const readyProject = response.data.find((p) => p.status === "ready");
      if (readyProject) {
        setSelectedProjectId(readyProject.id);
      }
    } catch (error) {
      console.error("Failed to load projects:", error);
      setError("Failed to load projects");
    } finally {
      setProjectsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedProjectId) {
      setError("Please select a project");
      return;
    }
    if (task.length < 10) {
      setError("Task description must be at least 10 characters");
      return;
    }
    if (selectedProject?.status !== "ready") {
      setError("Selected project is not ready for planning");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await plansApi.generate({
        project_id: selectedProjectId,
        task: task,
      });
      navigate(`/plan/${response.data.id}`);
    } catch (error) {
      console.error("Failed to generate plan:", error);
      setError("Failed to generate plan. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const isFormValid =
    selectedProjectId &&
    task.length >= 10 &&
    selectedProject?.status === "ready" &&
    !loading;

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate("/")}
          className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Projects
        </button>
        <h1 className="text-3xl font-bold text-white">Generate Plan</h1>
        <p className="text-slate-400 mt-1">
          Describe your task and let AI create an implementation plan
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Project Selector */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Select Project
          </label>
          {projectsLoading ? (
            <div className="flex items-center gap-2 text-slate-400">
              <Loader2 className="w-4 h-4 animate-spin" />
              Loading projects...
            </div>
          ) : projects.length === 0 ? (
            <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
              <p className="text-slate-400">No projects available.</p>
              <button
                type="button"
                onClick={() => navigate("/")}
                className="text-sky-400 hover:text-sky-300 mt-2"
              >
                Create a project first →
              </button>
            </div>
          ) : (
            <div className="relative">
              <select
                value={selectedProjectId}
                onChange={(e) => setSelectedProjectId(e.target.value)}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white appearance-none cursor-pointer focus:outline-none focus:border-sky-500"
                disabled={loading}
              >
                <option value="">Select a project...</option>
                {projects.map((project) => (
                  <option
                    key={project.id}
                    value={project.id}
                    disabled={project.status !== "ready"}
                  >
                    {project.name} {project.status !== "ready" ? `(${project.status})` : ""}
                  </option>
                ))}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
            </div>
          )}
          {selectedProject && selectedProject.status !== "ready" && (
            <p className="mt-2 text-sm text-yellow-400">
              This project needs to be indexed before generating plans.
            </p>
          )}
        </div>

        {/* Task Description */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Task Description
          </label>
          <textarea
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Describe what you want to implement... (minimum 10 characters)"
            rows={6}
            className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-500 resize-none focus:outline-none focus:border-sky-500"
            disabled={loading}
          />
          <div className="flex justify-between mt-2">
            <p className="text-sm text-slate-500">
              Be specific about what you want to achieve
            </p>
            <p className={`text-sm ${task.length < 10 ? "text-slate-500" : "text-green-400"}`}>
              {task.length}/10 min
            </p>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!isFormValid}
          className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-sky-500 hover:bg-sky-600 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
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
      </form>

      {/* Tips */}
      <div className="mt-8 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
        <h3 className="text-sm font-medium text-slate-300 mb-2">💡 Tips for better results</h3>
        <ul className="text-sm text-slate-400 space-y-1">
          <li>• Be specific about the feature or bug you want to address</li>
          <li>• Mention relevant files or components if you know them</li>
          <li>• Describe the expected behavior or outcome</li>
        </ul>
      </div>
    </div>
  );
}
