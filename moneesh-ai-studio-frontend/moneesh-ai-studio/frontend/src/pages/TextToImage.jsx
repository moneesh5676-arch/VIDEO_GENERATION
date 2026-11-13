import { useState } from "react";
import { Download, ImagePlus, Loader2, Sparkles } from "lucide-react";
import { api, mediaUrl } from "../lib/api.js";

export default function TextToImage() {
  const [prompt, setPrompt] = useState("");
  const [imageUrl, setImageUrl] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!prompt.trim()) return;

    setSubmitting(true);
    setError(null);
    setImageUrl(null);
    try {
      const result = await api.createTextImage({ prompt: prompt.trim() });
      setImageUrl(mediaUrl(result.image_url));
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1 className="font-display text-3xl font-bold text-white">Text to Image</h1>
      <p className="mt-1 text-zinc-500">Describe an image and create it with AI.</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-5">
        <form onSubmit={handleSubmit} className="card space-y-6 p-6 lg:col-span-3">
          <div>
            <label htmlFor="image-prompt" className="label">Prompt</label>
            <textarea
              id="image-prompt"
              rows={7}
              maxLength={1000}
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              placeholder="A cinematic portrait of a golden retriever in warm sunset light..."
              className="input resize-none"
            />
            <p className="mt-1 text-right text-xs text-zinc-600">{prompt.length}/1000</p>
          </div>

          <button type="submit" disabled={submitting || !prompt.trim()} className="btn-primary w-full">
            {submitting ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {submitting ? "Creating image…" : "Create Image"}
          </button>
        </form>

        <section className="card p-5 lg:col-span-2" aria-live="polite">
          <h2 className="mb-4 font-display text-lg font-semibold text-white">Preview</h2>
          <div className="grid min-h-72 place-items-center overflow-hidden rounded-xl border border-white/5 bg-ink-900">
            {imageUrl ? (
              <img src={imageUrl} alt={prompt} className="h-full w-full object-contain" />
            ) : submitting ? (
              <div className="flex flex-col items-center gap-3 text-zinc-400">
                <Loader2 size={32} className="animate-spin text-accent-purple" />
                <p className="text-sm">Creating your image…</p>
              </div>
            ) : error ? (
              <p className="px-6 text-center text-sm text-red-300">{error}</p>
            ) : (
              <div className="flex flex-col items-center gap-3 text-zinc-600">
                <ImagePlus size={34} />
                <p className="text-sm">Your generated image will appear here</p>
              </div>
            )}
          </div>
          {imageUrl && (
            <a href={imageUrl} download className="btn-ghost mt-4 w-full">
              <Download size={16} /> Download image
            </a>
          )}
        </section>
      </div>
    </div>
  );
}
