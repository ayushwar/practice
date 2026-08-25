/**
 * Soft, blurred gradient shapes drifting slowly in the background.
 * Purely decorative - pointer-events disabled so they never block clicks.
 * This is the app's signature visual motif: a hint that mood is fluid
 * and always gently shifting, rather than one fixed dot on a scale.
 */
export default function MoodOrbs() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 overflow-hidden z-0"
    >
      <div className="absolute -top-24 -left-20 h-72 w-72 rounded-blob bg-rose-400/30 blur-3xl animate-drift" />
      <div className="absolute top-1/3 -right-24 h-80 w-80 rounded-blob bg-lavender-400/30 blur-3xl animate-drift-slow" />
      <div className="absolute bottom-[-6rem] left-1/4 h-72 w-72 rounded-blob bg-peach-300/40 blur-3xl animate-drift" />
      <div className="absolute bottom-10 right-10 h-40 w-40 rounded-blob bg-rose-400/20 blur-2xl animate-drift-slow" />
    </div>
  );
}
