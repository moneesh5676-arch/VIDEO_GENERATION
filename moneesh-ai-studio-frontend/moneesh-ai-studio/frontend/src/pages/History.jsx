import { useState } from "react";
import { Link } from "react-router-dom";
import { AlertCircle, RefreshCw } from "lucide-react";
import useProjects from "../hooks/useProjects.js";
import ProjectCard from "../components/ProjectCard.jsx";

export default function History() {
  const { projects, loading, error, refresh, remove } = useProjects();
  const [deleteError, setDeleteError] = useState(null);

  async function handleDelete(project) {
    if (!window.confirm("Delete this project? This cannot be undone.")) return;
    setDeleteError(null);
    try {
      await remove(project.id);
    } catch (e) {
      setDeleteError(e.message);
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl font-bold text-white">Projects</h1>
          <p className="mt-1 text-zinc-500">All your generated videos.</p>
        </div>
        <button onClick={refresh} className="btn-ghost" disabled={loading}>
          <RefreshCw size={15} className={loading ? "animate-spin" : ""} /> Refresh
        </button>
      </div>

      {(error || deleteError) && (
        <div className="card mt-6 flex items-start gap-3 p-5 text-sm text-amber-300/90">
          <AlertCircle size={18} className="mt-0.5 shrink-0" />
          <p>{error || deleteError}</p>
        </div>
      )}

      {!loading && !error && projects.length === 0 ? (
        <div className="card mt-6 p-12 text-center text-zinc-500">
          Nothing here yet.{" "}
          <Link to="/text-to-video" className="text-accent-purple hover:underline">Create your first video</Link>.
        </div>
      ) : (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {projects.map((p) => (
            <ProjectCard key={p.id} project={p} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
