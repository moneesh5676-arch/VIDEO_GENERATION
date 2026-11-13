import { Link } from "react-router-dom";
import { Sparkles, Type, ImagePlay, ArrowRight, AlertCircle } from "lucide-react";
import useProjects from "../hooks/useProjects.js";
import ProjectCard from "../components/ProjectCard.jsx";

function SkeletonCard() {
  return (
    <div className="card overflow-hidden">
      <div className="aspect-video animate-shimmer bg-gradient-to-r from-ink-800 via-ink-700 to-ink-800 bg-[length:800px_100%]" />
      <div className="space-y-2 p-4">
        <div className="h-3 w-3/4 rounded bg-ink-700" />
        <div className="h-3 w-1/2 rounded bg-ink-700" />
      </div>
    </div>
  );
}

export default function Dashboard() {
  const { projects, loading, error } = useProjects();
  const recent = projects.slice(0, 4);

  return (
    <div className="space-y-10">
      {/* Hero */}
      <section className="relative overflow-hidden rounded-3xl border border-white/5 bg-gradient-to-br from-accent-purple/20 via-ink-800 to-accent-blue/20 p-8 sm:p-12">
        <div className="pointer-events-none absolute -right-20 -top-20 h-72 w-72 rounded-full bg-accent-purple/20 blur-3xl" />
        <div className="relative max-w-2xl">
          <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/30 px-3 py-1 text-xs font-medium text-zinc-300">
            <Sparkles size={13} className="text-accent-purple" /> Cinematic AI video studio
          </span>
          <h1 className="mt-5 font-display text-3xl font-bold leading-tight text-white sm:text-5xl">
            Turn words into <span className="bg-gradient-to-r from-accent-purple to-accent-blue bg-clip-text text-transparent">cinema</span>.
          </h1>
          <p className="mt-4 text-zinc-400">
            Write a prompt or upload an image and generate realistic video scenes using AI models running on your configured cloud provider.
          </p>
          <Link to="/text-to-video" className="btn-primary mt-7 inline-flex">
            <Sparkles size={16} /> Create Video
          </Link>
        </div>
      </section>

      {/* Quick actions */}
      <section className="grid gap-4 sm:grid-cols-2">
        {[
          { to: "/text-to-video", icon: Type, title: "Text to Video", desc: "Describe a scene and generate it." },
          { to: "/image-to-video", icon: ImagePlay, title: "Image to Video", desc: "Bring a still image to life." },
        ].map(({ to, icon: Icon, title, desc }) => (
          <Link key={to} to={to} className="card group flex items-center gap-4 p-5 transition hover:-translate-y-0.5 hover:border-accent-purple/30">
            <div className="grid h-12 w-12 place-items-center rounded-xl bg-accent-purple/15 text-accent-purple">
              <Icon size={22} />
            </div>
            <div className="flex-1">
              <p className="font-display font-semibold text-white">{title}</p>
              <p className="text-sm text-zinc-500">{desc}</p>
            </div>
            <ArrowRight size={18} className="text-zinc-600 transition group-hover:translate-x-1 group-hover:text-accent-purple" />
          </Link>
        ))}
      </section>

      {/* Recent projects */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-display text-xl font-semibold text-white">Recent projects</h2>
          <Link to="/projects" className="text-sm text-accent-purple hover:underline">View all</Link>
        </div>

        {loading ? (
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {[0, 1, 2, 3].map((i) => <SkeletonCard key={i} />)}
          </div>
        ) : error ? (
          <div className="card flex items-start gap-3 p-5 text-sm text-amber-300/90">
            <AlertCircle size={18} className="mt-0.5 shrink-0" />
            <p>{error}</p>
          </div>
        ) : recent.length === 0 ? (
          <div className="card p-10 text-center text-zinc-500">
            No projects yet. Click <span className="text-zinc-300">Create Video</span> to make your first one.
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {recent.map((p) => <ProjectCard key={p.id} project={p} />)}
          </div>
        )}
      </section>
    </div>
  );
}
