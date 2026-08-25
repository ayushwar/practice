import { useNavigate } from "react-router-dom";
import { Sparkles, ArrowRight, HeartHandshake } from "lucide-react";

export default function Home() {
  const navigate = useNavigate();

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-16">
      <div className="glass-card w-full max-w-md rounded-[2rem] px-8 py-10 text-center animate-rise">
        <div className="flex justify-center mb-6">
          <div className="relative h-16 w-16">
            <div className="absolute inset-0 rounded-blob bg-gradient-to-br from-rose-400 via-lavender-400 to-peach-400 animate-pulse-soft" />
            <div className="absolute inset-0 flex items-center justify-center">
              <Sparkles className="text-white" size={26} />
            </div>
          </div>
        </div>

        <p className="text-xs font-semibold tracking-[0.25em] uppercase text-rose-500 mb-3">
          Mahila Mitra
        </p>

        <h1 className="font-display text-3xl sm:text-4xl leading-tight text-ink mb-4">
          Let's Find Out How
          <br />
          You're Feeling Today
        </h1>

        <p className="text-ink-soft mb-8">
          A few questions. One little mood check.
        </p>

        <button
          type="button"
          onClick={() => navigate("/quiz")}
          className="group inline-flex items-center gap-2 bg-gradient-to-r from-rose-500 to-lavender-400 text-white font-semibold px-7 py-3.5 rounded-full shadow-soft hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
        >
          Start Mood Check
          <ArrowRight
            size={18}
            className="transition-transform group-hover:translate-x-1"
          />
        </button>

        <div className="mt-8 flex items-center justify-center gap-2 text-xs text-ink-muted">
          <HeartHandshake size={14} />
          <span>Made for fun — not a medical or psychological diagnosis.</span>
        </div>
      </div>
    </main>
  );
}
