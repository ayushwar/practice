import { useEffect, useState } from "react";
import {
  Smile,
  Meh,
  Frown,
  Zap,
  Coffee,
  CloudRain,
  BrainCircuit,
  Flame,
  MoonStar,
  MessageCircle,
  DoorClosed,
  PartyPopper,
  BatteryMedium,
} from "lucide-react";

const MOOD_ICONS = {
  Happy: Smile,
  Normal: Meh,
  Excited: Zap,
  Tired: Coffee,
  Bored: CloudRain,
  Overthinking: BrainCircuit,
  Low: Frown,
  Irritated: Flame,
  Quiet: MoonStar,
  Talkative: MessageCircle,
  "Needs Space": DoorClosed,
  Playful: PartyPopper,
};

const LEVEL_ORDER = { Low: 1, Medium: 2, High: 3, "Very High": 4 };

function LevelPill({ level }) {
  const tone =
    LEVEL_ORDER[level] >= 4
      ? "bg-rose-500 text-white"
      : LEVEL_ORDER[level] === 3
      ? "bg-rose-400/80 text-white"
      : LEVEL_ORDER[level] === 2
      ? "bg-peach-300/80 text-ink"
      : "bg-lavender-100 text-ink-soft";

  return (
    <span
      className={`inline-block px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase ${tone}`}
    >
      {level}
    </span>
  );
}

function AnimatedBar({ percent, level }) {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const timeout = setTimeout(() => setWidth(percent), 150);
    return () => clearTimeout(timeout);
  }, [percent]);

  return (
    <div>
      <div className="h-3 w-full rounded-full bg-white/70 overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-lavender-400 to-rose-400 transition-all duration-[1200ms] ease-out"
          style={{ width: `${width}%` }}
        />
      </div>
      <div className="flex items-center justify-between mt-1.5">
        <span className="text-xs text-ink-muted">{percent}%</span>
        <LevelPill level={level} />
      </div>
    </div>
  );
}

export default function MoodResult({ result }) {
  if (!result) return null;

  const {
    primaryMood,
    secondaryMood,
    energy,
    socialBattery,
    socialLevel,
    overthinking,
    message,
    answerSummary,
  } = result;

  const PrimaryIcon = MOOD_ICONS[primaryMood] || Meh;

  return (
    <div className="w-full animate-rise">
      {/* Mood badge */}
      <div className="flex flex-col items-center text-center mb-6">
        <div className="relative h-24 w-24 mb-4 animate-pop-in">
          <div className="absolute inset-0 rounded-blob bg-gradient-to-br from-rose-400 via-lavender-400 to-peach-400 shadow-soft" />
          <div className="absolute inset-0 flex items-center justify-center">
            <PrimaryIcon className="text-white" size={34} strokeWidth={2} />
          </div>
        </div>

        <p className="text-sm sm:text-base font-medium text-ink-soft mb-2">
          So, meri Mahila Mitra ka mood...
        </p>
        <h1 className="font-display text-3xl sm:text-4xl text-ink tracking-wide uppercase">
          {primaryMood}
          {secondaryMood ? (
            <span className="text-rose-500"> + {secondaryMood}</span>
          ) : null}
        </h1>
        <p className="mt-4 max-w-sm text-ink-soft leading-relaxed">
          {message}
        </p>
      </div>

      {/* Stats */}
      <div className="glass-card rounded-3xl p-6 space-y-5 mb-6">
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-sm font-semibold text-ink">Energy</span>
          </div>
          <LevelPill level={energy} />
        </div>

        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <BatteryMedium size={16} className="text-ink-soft" />
            <span className="text-sm font-semibold text-ink">
              Social Battery
            </span>
          </div>
          <AnimatedBar percent={socialBattery} level={socialLevel} />
        </div>

        <div>
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-sm font-semibold text-ink">
              Overthinking
            </span>
          </div>
          <LevelPill level={overthinking} />
        </div>
      </div>

      {/* Answer summary */}
      {answerSummary && answerSummary.length > 0 && (
        <details className="glass-card rounded-3xl px-6 py-4 mb-2 group">
          <summary className="cursor-pointer text-sm font-semibold text-ink-soft select-none">
            Based on your answers
          </summary>
          <ul className="mt-3 space-y-1.5">
            {answerSummary.map((item) => (
              <li
                key={item.question}
                className="text-sm text-ink-muted flex justify-between gap-4"
              >
                <span className="capitalize">{item.question}</span>
                <span className="text-ink-soft font-medium">
                  {item.answer}
                </span>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
