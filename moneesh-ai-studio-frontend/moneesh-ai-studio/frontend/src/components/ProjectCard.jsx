import { Trash2, Film } from "lucide-react";
import StatusBadge from "./StatusBadge.jsx";
import { mediaUrl } from "../lib/api.js";

export default function ProjectCard({ project, onDelete }) {
  const thumb = mediaUrl(project.thumbnail_url);
  const date = project.created_at ? new Date(project.created_at).toLocaleString() : "";

  return (
    <article className="card group overflow-hidden transition hover:-translate-y-1 hover:border-accent-purple/30">
      <div className="relative aspect-video bg-gradient-to-br from-ink-700 to-ink-900">
        {thumb ? (
          <img src={thumb} alt="" className="h-full w-full object-cover" loading="lazy" />
        ) : (
          <div className="grid h-full place-items-center text-zinc-600">
            <Film size={30} />
          </div>
        )}
        <div className="absolute left-3 top-3">
          <StatusBadge status={project.status} />
        </div>
      </div>
      <div className="p-4">
        <p className="line-clamp-2 min-h-[2.5rem] text-sm text-zinc-200">
          {project.prompt || "Untitled project"}
        </p>
        <div className="mt-3 flex items-center justify-between text-xs text-zinc-500">
          <span>
            {[project.aspect_ratio, project.resolution, project.duration && `${project.duration}s`]
              .filter(Boolean)
              .join(" · ")}
          </span>
          {onDelete && (
            <button
              onClick={() => onDelete(project)}
              className="rounded-lg p-1.5 text-zinc-500 transition hover:bg-red-500/10 hover:text-red-400"
              aria-label="Delete project"
            >
              <Trash2 size={15} />
            </button>
          )}
        </div>
        {date && <p className="mt-1 text-[11px] text-zinc-600">{date}</p>}
      </div>
    </article>
  );
}
