import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, Loader2, Trash2, Play, FileText, X, AlertTriangle } from "lucide-react";
import { projectsApi, Project } from "../services/api";

export default function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: "", path: "" });
  const [indexingIds, setIndexingIds] = useState<Set<string>>(new Set());
  const [deleteModal, setDeleteModal] = useState<{ show: boolean; project: Project | null }>({
    show: false,
    project: null,
  });
  const pollIntervalsRef = useRef<Map<string, ReturnType<typeof setInterval>>>(new Map());

  useEffect(() => {
    loadProjects();

    return () => {
      pollIntervalsRef.current.forEach((intervalId) => {
        clearInterval(intervalId);
      });
      pollIntervalsRef.current.clear();
    };
  }, []);

  const loadProjects = async () => {
    try {
      const response = await projectsApi.list();
      setProjects(response.data);
    } catch (error) {
      console.error("Failed to load projects:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.path) return;

    try {
      await projectsApi.create(formData);
      setFormData({ name: "", path: "" });
      setShowForm(false);
      await loadProjects();
    } catch (error) {
      console.error("Failed to create project:", error);
      alert("Project creation failed. Please check that the path is correct.");
    }
  };

  const handleIndex = async (id: string) => {
    setIndexingIds((prev) => new Set(prev).add(id));

    try {
      await projectsApi.index(id);

      // Poll for indexing status
      const pollInterval = setInterval(async () => {
        try {
          const response = await projectsApi.get(id);
          const project = response.data;

          // Update project in list
          setProjects((prev) =>
            prev.map((p) => (p.id === id ? project : p))
          );

          // Stop polling when indexing is complete
          if (project.status === "ready" || project.status === "error") {
            clearInterval(pollInterval);
            pollIntervalsRef.current.delete(id);
            setIndexingIds((prev) => {
              if (!prev.has(id)) return prev;
              const next = new Set(prev);
              next.delete(id);
              return next;
            });
          }
        } catch (error) {
          clearInterval(pollInterval);
          pollIntervalsRef.current.delete(id);
          setIndexingIds((prev) => {
            if (!prev.has(id)) return prev;
            const next = new Set(prev);
            next.delete(id);
            return next;
          });
        }
      }, 2000);

      pollIntervalsRef.current.set(id, pollInterval);
    } catch (error) {
      console.error("Failed to start indexing:", error);
      setIndexingIds((prev) => {
        if (!prev.has(id)) return prev;
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await projectsApi.delete(id);
      setDeleteModal({ show: false, project: null });
      await loadProjects();
    } catch (error) {
      console.error("Failed to delete project:", error);
      alert("Failed to delete project.");
    }
  };

  const openDeleteModal = (project: Project) => {
    setDeleteModal({ show: true, project });
  };

  const closeDeleteModal = () => {
    setDeleteModal({ show: false, project: null });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      </div>
    );
  }

  return (
    <div>
      {/* Delete Confirmation Modal */}
      {deleteModal.show && deleteModal.project && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={closeDeleteModal}
          />
          {/* Modal */}
          <div className="relative bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-md mx-4 shadow-2xl">
            <button
              onClick={closeDeleteModal}
              className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-red-500/20 rounded-full">
                <AlertTriangle className="w-6 h-6 text-red-400" />
              </div>
              <h2 className="text-xl font-semibold text-white">Delete Project</h2>
            </div>
            
            <p className="text-slate-300 mb-2">
              Are you sure you want to delete this project?
            </p>
            <p className="text-sm text-slate-400 mb-6">
              <span className="font-semibold text-white">{deleteModal.project.name}</span>
              <br />
              <span className="font-mono text-xs">{deleteModal.project.path}</span>
            </p>
            <p className="text-sm text-red-400 mb-6">
              This action cannot be undone. All indexed data will be permanently removed.
            </p>
            
            <div className="flex gap-3 justify-end">
              <button
                onClick={closeDeleteModal}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDelete(deleteModal.project!.id)}
                className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Projects</h1>
          <p className="text-slate-400 mt-1">
            Manage your codebases for AI analysis
          </p>
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
        <div className="mb-8 p-6 bg-slate-800 rounded-xl border border-slate-700">
          <h2 className="text-xl font-semibold text-white mb-4">Add New Project</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Project Name
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="My Awesome Project"
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
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
                placeholder="/path/to/your/project"
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                required
              />
            </div>
            <div className="flex gap-3">
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
        </div>
      )}

      {/* Projects List */}
      {projects.length === 0 ? (
        <div className="text-center py-16 bg-slate-800/50 rounded-xl border border-slate-700">
          <h3 className="text-xl font-medium text-slate-400 mb-2">No projects yet</h3>
          <p className="text-slate-500">Add a project to get started</p>
        </div>
      ) : (
        <div className="space-y-4">
          {projects.map((project) => (
            <div
              key={project.id}
              className="p-6 bg-slate-800 rounded-xl border border-slate-700"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-white">{project.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${project.status === 'ready' ? 'bg-green-500/20 text-green-400' :
                      project.status === 'indexing' ? 'bg-blue-500/20 text-blue-400' :
                        'bg-yellow-500/20 text-yellow-400'
                      }`}>
                      {project.status}
                    </span>
                  </div>
                  <p className="text-sm text-slate-400 font-mono">{project.path}</p>
                  <p className="text-sm text-slate-500 mt-1">{project.file_count} files indexed</p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => navigate(`/task/${project.id}`)}
                    disabled={project.status !== "ready"}
                    className="p-2 bg-sky-500/20 hover:bg-sky-500/30 disabled:opacity-50 disabled:cursor-not-allowed text-sky-400 rounded-lg transition-colors"
                    title="Create Plan"
                  >
                    <FileText className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleIndex(project.id)}
                    disabled={indexingIds.has(project.id) || project.status === "indexing" || project.status === "ready"}
                    className="p-2 bg-emerald-500/20 hover:bg-emerald-500/30 disabled:opacity-50 disabled:cursor-not-allowed text-emerald-400 rounded-lg transition-colors"
                    title="Start Indexing"
                  >
                    {indexingIds.has(project.id) || project.status === "indexing" ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Play className="w-4 h-4" />
                    )}
                  </button>
                  <button
                    onClick={() => openDeleteModal(project)}
                    className="p-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
                    title="Delete Project"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
