const COLAB_NOTEBOOK_URL =
  "https://colab.research.google.com/github/moneesh5676-arch/VIDEO_GENERATION/blob/main/free_colab_video_generator.ipynb";

export const DURATIONS = [4, 6, 8].map((duration) => ({
  value: duration,
  label: `${duration}s`,
}));

export default function TextToVideo() {
  return (
    <div>
      <h1 className="font-display text-3xl font-bold text-white">Free Text to Video</h1>
      <p className="mt-1 text-zinc-500">
        Generate a video in a temporary Google Colab session without an API key or provider credits.
      </p>

      <section className="card mt-8 max-w-3xl space-y-5 p-6">
        <div>
          <h2 className="text-xl font-semibold text-white">Open the free generator</h2>
          <p className="mt-2 text-sm text-zinc-400">
            The notebook uses the open-source CogVideoX-2B model. In Colab, choose a T4 GPU if one is
            available, run the cells in order, and download the resulting MP4.
          </p>
        </div>

        <a
          href={COLAB_NOTEBOOK_URL}
          target="_blank"
          rel="noreferrer"
          className="btn-primary inline-flex"
        >
          Open Google Colab notebook
        </a>

        <p className="text-xs text-zinc-500">
          Free GPU access is limited and not guaranteed. Generation may be slow or run out of memory.
          This is a separate manual workflow, not an always-on backend service.
        </p>
      </section>
    </div>
  );
}
