import { useState, useEffect } from "react";
import { Plus, Loader2 } from "lucide-react";

export default function Projects() {
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    // TODO: Fetch projects from API using projectsApi.list()
    // TODO: Set projects state and loading state
    setLoading(false);
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Create project using projectsApi.create(formData)
    // TODO: Reset form and reload projects
  };

  const handleIndex = async (id: string) => {
    // TODO: Start indexing using projectsApi.index(id)
    // TODO: Implement polling to check indexing status
    // Hint: Use setInterval to periodically call projectsApi.get(id)
  };

  const handleDelete = async (id: string) => {
    // TODO: Confirm deletion with user
    // TODO: Delete project using projectsApi.delete(id)
    // TODO: Reload projects
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

      {/* TODO: Add Project Form - implement form UI */}
      {/* TODO: Projects List - display projects with actions */}
    </div>
  );
}
