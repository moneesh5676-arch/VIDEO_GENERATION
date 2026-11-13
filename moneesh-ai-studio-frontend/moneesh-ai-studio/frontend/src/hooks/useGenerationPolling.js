import { useEffect } from "react";
import { api } from "../lib/api.js";

export default function useGenerationPolling(project, setProject, setError) {
  useEffect(() => {
    if (!project || !["queued", "processing"].includes(project.status)) return undefined;

    let cancelled = false;
    let timeoutId;

    async function poll() {
      try {
        const latest = await api.getProject(project.id);
        if (cancelled) return;
        setProject(latest);
        if (latest.status === "queued" || latest.status === "processing") {
          timeoutId = window.setTimeout(poll, 2000);
        }
      } catch (err) {
        if (cancelled) return;
        setProject(null);
        setError(err.message);
      }
    }

    timeoutId = window.setTimeout(poll, 1500);
    return () => {
      cancelled = true;
      window.clearTimeout(timeoutId);
    };
  }, [project?.id, project?.status, setProject, setError]);
}
