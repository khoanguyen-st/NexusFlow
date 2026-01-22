import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Loader2 } from "lucide-react";

export default function PlanView() {
  const { planId } = useParams<{ planId: string }>();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (planId) {
      loadPlan(planId);
    }
  }, [planId]);

  const loadPlan = async (id: string) => {
    // TODO: Load plan using plansApi.get(id)
    // TODO: Set plan state and loading state
    setLoading(false);
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
      {/* TODO: Add header with back button */}
      {/* TODO: Display plan summary */}
      {/* TODO: Display affected files with action badges */}
      {/* TODO: Display implementation steps */}
      {/* TODO: Display reusable components */}
      {/* TODO: Display confidence score */}

      <div className="text-center py-16">
        <h2 className="text-2xl text-white mb-4">Plan View Page</h2>
        <p className="text-slate-400">TODO: Implement plan display UI</p>
        <p className="text-sm text-slate-500 mt-2">
          Refer to task.md Section 2.3 - Plan Display Page
        </p>
      </div>
    </div>
  );
}
