import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { RotateCcw } from "lucide-react";
import MoodResult from "../components/MoodResult.jsx";

export default function Result({ result, setAnswers, setResult }) {
  const navigate = useNavigate();

  useEffect(() => {
    if (!result) {
      navigate("/", { replace: true });
    }
  }, [result, navigate]);

  if (!result) return null;

  const restart = () => {
    setAnswers({});
    setResult(null);
    navigate("/quiz");
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-16">
      <div className="w-full max-w-md">
        <MoodResult result={result} />

        <div className="flex flex-col items-center gap-3 mt-4">
          <button
            type="button"
            onClick={restart}
            className="inline-flex items-center gap-2 bg-gradient-to-r from-rose-500 to-lavender-400 text-white font-semibold px-7 py-3.5 rounded-full shadow-soft hover:-translate-y-0.5 transition-all duration-200"
          >
            <RotateCcw size={16} />
            Take Quiz Again
          </button>
          <p className="text-xs text-ink-muted">
            Made for fun — not a medical or psychological diagnosis.
          </p>
        </div>
      </div>
    </main>
  );
}
