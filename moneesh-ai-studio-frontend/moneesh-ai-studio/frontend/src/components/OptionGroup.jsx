export default function OptionGroup({ label, options, value, onChange }) {
  return (
    <div>
      <span className="label">{label}</span>
      <div className="flex flex-wrap gap-2">
        {options.map((opt) => {
          const active = opt.value === value;
          return (
            <button
              key={opt.value}
              type="button"
              onClick={() => onChange(opt.value)}
              className={`rounded-xl border px-4 py-2 text-sm font-medium transition ${
                active
                  ? "border-accent-purple/60 bg-accent-purple/15 text-white"
                  : "border-white/10 bg-ink-900 text-zinc-400 hover:border-white/20 hover:text-zinc-200"
              }`}
            >
              {opt.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
