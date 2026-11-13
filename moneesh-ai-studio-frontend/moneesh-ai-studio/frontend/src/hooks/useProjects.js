import { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api.js";

export default function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listProjects();
      setProjects(Array.isArray(data) ? data : []);
    } catch (e) {
      setProjects([]);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const remove = useCallback(async (id) => {
    await api.deleteProject(id);
    setProjects((prev) => prev.filter((p) => p.id !== id));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { projects, loading, error, refresh, remove };
}
