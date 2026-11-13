import { useEffect, useRef, useState } from "react";
import { Upload, Sparkles, Loader2, X } from "lucide-react";
import OptionGroup from "../components/OptionGroup.jsx";
import PreviewPanel from "../components/PreviewPanel.jsx";
import { ASPECTS, DURATIONS, RESOLUTIONS } from "./TextToVideo.jsx";
import { api } from "../lib/api.js";

const MAX_MB = 10;

export default function ImageToVideo() {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [instructions, setInstructions] = useState("");
  const [duration, setDuration] = useState(5);
  const [aspect, setAspect] = useState("16:9");
  const [resolution, setResolution] = useState("720p");
  const [submitting, setSubmitting] = useState(false);
  const [project, setProject] = useState(null);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);

  useEffect(() => () => preview && URL.revokeObjectURL(preview), [preview]);

  function pick(f) {
    if (!f) return;
    if (!/^image\/(png|jpe?g|webp)$/.test(f.type)) return setError("Please upload a PNG, JPG or WEBP image.");
    if (f.size > MAX_MB * 1024 * 1024) return setError(`Image must be smaller than ${MAX_MB} MB.`);
    setError(null);
    setFile(f);
    setPreview(URL.createObjectURL(f));
  }

  function clear() {
    setFile(null);
    setPreview(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setSubmitting(true);
    setError(null);
    setProject(null);
    try {
      const fd = new FormData();
      fd.append("image", file);
      fd.append("prompt", instructions.trim());
      fd.append("duration", duration);
      fd.append("aspect_ratio", aspect);
      fd.append("resolution", resolution);
      setProject(await api.createImageVideo(fd));
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1 className="font-display text-3xl font-bold text-white">Image to Video</h1>
      <p className="mt-1 text-zinc-500">Upload an image and describe how it should move.</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-5">
        <form onSubmit={handleSubmit} className="card space-y-6 p-6 lg:col-span-3">
          <div>
            <span className="label">Source image</span>
            {preview ? (
              <div className="relative overflow-hidden rounded-xl border border-white/10">
                <img src={preview} alt="Upload preview" className="max-h-72 w-full object-contain bg-ink-900" />
                <button
                  type="button"
                  onClick={clear}
                  className="absolute right-3 top-3 rounded-full bg-black/70 p-1.5 text-white hover:bg-black"
                  aria-label="Remove image"
                >
                  <X size={16} />
                </button>
              </div>
            ) : (
              <div
                onClick={() => inputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                onDragLeave={() => setDragging(false)}
                onDrop={(e) => { e.preventDefault(); setDragging(false); pick(e.dataTransfer.files?.[0]); }}
                className={`flex cursor-pointer flex-col items-center gap-2 rounded-xl border-2 border-dashed px-6 py-12 text-center transition ${
                  dragging ? "border-accent-purple bg-accent-purple/10" : "border-white/10 hover:border-accent-purple/50"
                }`}
              >
                <Upload className="text-accent-purple" />
                <p className="text-sm text-zinc-300">Click or drag an image here</p>
                <p className="text-xs text-zinc-600">PNG, JPG or WEBP · max {MAX_MB} MB</p>
              </div>
            )}
            <input ref={inputRef} type="file" accept="image/png,image/jpeg,image/webp" hidden onChange={(e) => pick(e.target.files?.[0])} />
          </div>

          <div>
            <label htmlFor="instr" className="label">Animation instructions</label>
            <textarea
              id="instr"
              rows={4}
              maxLength={500}
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              placeholder="Slow cinematic push-in, hair gently moving in the wind, clouds drifting in the background…"
              className="input resize-none"
            />
          </div>

          <OptionGroup label="Duration" options={DURATIONS} value={duration} onChange={setDuration} />
          <OptionGroup label="Aspect ratio" options={ASPECTS} value={aspect} onChange={setAspect} />
          <OptionGroup label="Resolution" options={RESOLUTIONS} value={resolution} onChange={setResolution} />

          <button type="submit" disabled={submitting || !file} className="btn-primary w-full">
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
