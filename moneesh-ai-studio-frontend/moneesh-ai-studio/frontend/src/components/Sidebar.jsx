import { NavLink } from "react-router-dom";
import { LayoutDashboard, Type, ImagePlay, ImagePlus, FolderClock, Clapperboard, X } from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/text-to-video", label: "Text to Video", icon: Type },
  { to: "/text-to-image", label: "Text to Image", icon: ImagePlus },
  { to: "/image-to-video", label: "Image to Video", icon: ImagePlay },
  { to: "/projects", label: "Projects", icon: FolderClock },
];

export default function Sidebar({ open, onClose }) {
  return (
    <>
      {/* Mobile backdrop */}
      <div
        onClick={onClose}
        className={`fixed inset-0 z-30 bg-black/70 backdrop-blur-sm transition-opacity lg:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      />
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-white/5 bg-ink-900/95 p-5 backdrop-blur
        transition-transform duration-300 lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-accent-purple to-accent-blue shadow-lg shadow-accent-purple/30">
              <Clapperboard size={20} className="text-white" />
            </div>
            <div className="leading-tight">
              <p className="font-display text-base font-bold tracking-wide text-white">MONEESH</p>
              <p className="text-[10px] font-semibold uppercase tracking-[0.25em] text-accent-purple">AI Studio</p>
            </div>
          </div>
          <button onClick={onClose} className="text-zinc-400 hover:text-white lg:hidden" aria-label="Close menu">
            <X size={20} />
          </button>
        </div>

        <nav className="flex flex-1 flex-col gap-1">
          {links.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={onClose}
              className={({ isActive }) =>
                `group flex items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-gradient-to-r from-accent-purple/20 to-accent-blue/10 text-white ring-1 ring-accent-purple/30"
                    : "text-zinc-400 hover:bg-white/5 hover:text-zinc-100"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        <p className="mt-6 rounded-xl border border-white/5 bg-ink-800 p-3 text-xs leading-relaxed text-zinc-500">
          Free text-to-video runs in Colab when a GPU is available. Other AI features need an external provider.
        </p>
      </aside>
    </>
  );
}
