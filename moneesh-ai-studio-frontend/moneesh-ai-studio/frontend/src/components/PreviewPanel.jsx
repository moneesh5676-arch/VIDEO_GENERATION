import { Film, Loader2, Download, AlertTriangle } from "lucide-react";
import StatusBadge from "./StatusBadge.jsx";
import { mediaUrl } from "../lib/api.js";

const RATIOS = { "16:9": "16 / 9", "9:16": "9 / 16", "1:1": "1 / 1" };

/**
 * project: the backend project object (or null before anything is submitted)
 * error: error message string (or null)
 */
export default function PreviewPanel({ project, aspectRatio = "16:9", error }) {
  const src = mediaUrl(project?.video_url);
  const busy = project && (project.status === "queued" || project.status === "processing");

  return (
    <div className="card p-5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-lg font-semibold text-white">Preview</h3>
        {project && <StatusBadge status={project.status} />}
      </div>

      <div
        className="mx-auto grid w-full max-w-md place-items-center overflow-hidden rounded-xl border border-white/5 bg-ink-900"
        style={{ aspectRatio: RATIOS[aspectRatio] || RATIOS["16:9"], maxHeight: "60vh" }}
      >
        {src && project.status === "completed" ? (
          <video src={src} controls playsInline className="h-full w-full object-contain" />
        ) : busy ? (
          <div className="flex flex-col items-center gap-3 text-zinc-400">
            <Loader2 size={32} className="animate-spin text-accent-purple" />
            <p className="text-sm">Your video is being generated…</p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center gap-3 px-6 text-center text-red-300">
            <AlertTriangle size={28} />
            <p className="text-sm">{error}</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3 text-zinc-600">
            <Film size={34} />
            <p className="text-sm">Your generated video will appear here</p>
          </div>
        )}
      </div>

      {src && project?.status === "completed" && (
        <a href={src} download className="btn-ghost mt-4 w-full">
          <Download size={16} /> Download video
        </a>
      )}
    </div>
  );
}
