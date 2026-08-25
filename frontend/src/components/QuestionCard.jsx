import { Check } from "lucide-react";

export default function QuestionCard({ question, selectedValue, onSelect }) {
  return (
    <div key={question.id} className="animate-rise">
      <h2 className="font-display text-2xl sm:text-3xl text-ink mb-6 leading-snug">
        {question.text}
      </h2>

      <div className="flex flex-col gap-3">
        {question.options.map((option) => {
          const isSelected = selectedValue === option.value;
          return (
            <button
              key={option.value}
              type="button"
              role="radio"
              aria-checked={isSelected}
              onClick={() => onSelect(option.value)}
              className={`group flex items-center justify-between w-full text-left px-5 py-4 rounded-2xl border transition-all duration-200
                ${
                  isSelected
                    ? "bg-gradient-to-r from-rose-400 to-lavender-400 border-transparent text-white shadow-soft scale-[1.02]"
                    : "bg-white/70 border-white/80 text-ink hover:bg-white hover:-translate-y-0.5 hover:shadow-card"
                }`}
            >
              <span className="font-medium text-base sm:text-lg">
                {option.label}
              </span>
              <span
                className={`flex items-center justify-center h-6 w-6 rounded-full border-2 transition-all
                  ${
                    isSelected
                      ? "bg-white border-white"
                      : "border-ink-muted/40 group-hover:border-rose-400"
                  }`}
              >
                {isSelected && (
                  <Check size={14} strokeWidth={3} className="text-rose-500" />
                )}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
