import { useState } from "react";
import { Outlet, useLocation, Link } from "react-router-dom";
import { Menu, Plus } from "lucide-react";
import Sidebar from "./Sidebar.jsx";

export default function Layout() {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();

  return (
    <div className="min-h-screen">
      <Sidebar open={open} onClose={() => setOpen(false)} />

      <div className="lg:pl-64">
        {/* Top bar (mobile) */}
        <header className="sticky top-0 z-20 flex items-center justify-between border-b border-white/5 bg-ink-950/80 px-4 py-3 backdrop-blur lg:hidden">
          <button onClick={() => setOpen(true)} className="text-zinc-300" aria-label="Open menu">
            <Menu size={22} />
          </button>
          <span className="font-display font-bold tracking-wide text-white">MONEESH AI STUDIO</span>
          <Link to="/text-to-video" className="text-accent-purple" aria-label="Create video">
            <Plus size={22} />
          </Link>
        </header>

        <main key={pathname} className="mx-auto max-w-7xl animate-fade-up px-4 py-6 sm:px-8 sm:py-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
