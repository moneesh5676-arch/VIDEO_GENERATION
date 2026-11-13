import { useState } from "react";
import { Sparkles, Loader2 } from "lucide-react";
import OptionGroup from "../components/OptionGroup.jsx";
import PreviewPanel from "../components/PreviewPanel.jsx";
import { api } from "../lib/api.js";

export const ASPECTS = [
  { value: "16:9", label: "16:9 Landscape" },
  { value: "9:16", label: "9:16 Vertical" },
  { value: "1:1", label: "1:1 Square" },
];
export const DURATIONS = [3, 5, 8, 10].map((d) => ({ value: d, label: `${d}s` }));
export const RESOLUTIONS = ["480p", "720p", "1080p"].map((r) => ({ value: r, label: r }));

export default function TextToVideo() {
  const [prompt, setPrompt] = useState("");
  const [duration, setDuration] = useState(5);
  const [aspect, setAspect] = useState("16:9");
  const [resolution, setResolution] = useState("720p");
  const [submitting, setSubmitting] = useState(false);
  const [project, setProject] = useState(null);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setSubmitting(true);
    setError(null);
    setProject(null);
    try {
      const created = await api.createTextVideo({
        prompt: prompt.trim(),
        duration,
        aspect_ratio: aspect,
        resolution,
      });
      setProject(created); // status polling is added in Step 5
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1 className="font-display text-3xl font-bold text-white">Text to Video</h1>
      <p className="mt-1 text-zinc-500">Describe your scene in detail for the best cinematic results.</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-5">
        <form onSubmit={handleSubmit} className="card space-y-6 p-6 lg:col-span-3">
          <div>
            <label htmlFor="prompt" className="label">Prompt</label>
            <textarea
              id="prompt"
              rows={7}
              maxLength={1000}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="A lone astronaut walks across a red desert at golden hour, dust swirling, cinematic lighting, shallow depth of field, 35mm film look…"
              className="input resize-none"
            />
            <p className="mt-1 text-right text-xs text-zinc-600">{prompt.length}/1000</p>
          </div>

          <OptionGroup label="Duration" options={DURATIONS} value={duration} onChange={setDuration} />
          <OptionGroup label="Aspect ratio" options={ASPECTS} value={aspect} onChange={setAspect} />
          <OptionGroup label="Resolution" options={RESOLUTIONS} value={resolution} onChange={setResolution} />

          <button type="submit" disabled={submitting || !prompt.trim()} className="btn-primary w-full">
            {submitting ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {submitting ? "Submitting…" : "Generate Video"}
          </button>
        </form>

        <div className="lg:col-span-2">
          <PreviewPanel project={project} aspectRatio={aspect} error={error} />
        </div>
      </div>
    </div>
  );
}
