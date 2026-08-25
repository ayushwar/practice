export default function ProgressBar({ current, total }) {
  const percent = Math.round((current / total) * 100);

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold tracking-widest uppercase text-ink-muted">
          Question {current} of {total}
        </span>
        <span className="text-xs font-semibold text-rose-500">{percent}%</span>
      </div>
      <div className="h-2 w-full rounded-full bg-white/60 overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-rose-400 via-lavender-400 to-peach-400 transition-all duration-500 ease-out"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
