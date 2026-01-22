import { useEffect } from "react";
import { useParams } from "react-router-dom";

export default function TaskInput() {
  const { projectId } = useParams<{ projectId: string }>();

  useEffect(() => {
    if (projectId) {
      loadProject(projectId);
    }
  }, [projectId]);

  const loadProject = async (id: string) => {
    // TODO: Load project using projectsApi.get(id)
    // TODO: Set project state
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Validate task length (min 10 chars)
    // TODO: Call plansApi.generate() with project_id and task
    // TODO: Navigate to /plan/{planId} on success
    // TODO: Handle errors
  };

  return (
    <div>
      {/* TODO: Add header with back button */}
      {/* TODO: Add task input form with textarea */}
      {/* TODO: Add submit button with loading state */}

      <div className="text-center py-16">
        <h2 className="text-2xl text-white mb-4">Task Input Page</h2>
        <p className="text-slate-400">TODO: Implement task input form</p>
        <p className="text-sm text-slate-500 mt-2">
          Refer to task.md Section 2.3 - Task Input Page
        </p>
      </div>
    </div>
  );
}
