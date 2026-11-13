const BASE = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, options);
  } catch {
    throw new Error(
      `Cannot reach the backend at ${BASE}. Make sure the FastAPI server is running (added in Step 2).`
    );
  }
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      /* ignore non-JSON error bodies */
    }
    throw new Error(detail);
  }
  return res.status === 204 ? null : res.json();
}

/** Turn a backend-relative media path into an absolute URL. */
export const mediaUrl = (path) => (!path ? null : path.startsWith("http") ? path : `${BASE}${path}`);

export const api = {
  listProjects: () => request("/api/projects"),
  getProject: (id) => request(`/api/projects/${id}`),
  deleteProject: (id) => request(`/api/projects/${id}`, { method: "DELETE" }),

  createTextVideo: (payload) =>
    request("/api/generate/text-to-video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),

  createImageVideo: (formData) =>
    request("/api/generate/image-to-video", { method: "POST", body: formData }),
};
