import { CheckCircle2, Loader2, Clock, XCircle } from "lucide-react";

const styles = {
  queued: { cls: "bg-zinc-500/15 text-zinc-300", icon: Clock, label: "Queued" },
  processing: { cls: "bg-accent-blue/15 text-blue-300", icon: Loader2, label: "Generating", spin: true },
  completed: { cls: "bg-emerald-500/15 text-emerald-300", icon: CheckCircle2, label: "Completed" },
  failed: { cls: "bg-red-500/15 text-red-300", icon: XCircle, label: "Failed" },
};

export default function StatusBadge({ status = "queued" }) {
  const s = styles[status] || styles.queued;
  const Icon = s.icon;
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${s.cls}`}>
      <Icon size={12} className={s.spin ? "animate-spin" : ""} />
      {s.label}
    </span>
  );
}
