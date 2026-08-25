import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronLeft, ChevronRight, AlertCircle } from "lucide-react";
import ProgressBar from "../components/ProgressBar.jsx";
import QuestionCard from "../components/QuestionCard.jsx";
import LoadingScreen from "../components/LoadingScreen.jsx";
import { fetchQuestions, predictMood } from "../services/api.js";

const MIN_ANALYZING_MS = 1400;

export default function Quiz({ answers, setAnswers, setResult }) {
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [loadError, setLoadError] = useState(false);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    let isMounted = true;
    fetchQuestions()
      .then((data) => {
        if (isMounted) {
          setQuestions(data);
          setLoadingQuestions(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setLoadError(true);
          setLoadingQuestions(false);
        }
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const currentQuestion = questions[currentIndex];
  const isLastQuestion = currentIndex === questions.length - 1;
  const selectedValue = currentQuestion ? answers[currentQuestion.id] : undefined;

  const handleSelect = (value) => {
    setAnswers((prev) => ({ ...prev, [currentQuestion.id]: value }));
  };

  const goBack = () => {
    if (currentIndex > 0) setCurrentIndex((i) => i - 1);
    else navigate("/");
  };

  const submitQuiz = useCallback(async () => {
    setSubmitting(true);
    setSubmitError("");
    const startedAt = Date.now();

    try {
      const data = await predictMood(answers);
      const elapsed = Date.now() - startedAt;
      const remaining = Math.max(MIN_ANALYZING_MS - elapsed, 0);

      setTimeout(() => {
        setResult(data);
        navigate("/result");
      }, remaining);
    } catch (err) {
      setTimeout(() => {
        setSubmitting(false);
        setSubmitError("Couldn't read your mood right now. Try again.");
      }, MIN_ANALYZING_MS);
    }
  }, [answers, navigate, setResult]);

  const goNext = () => {
    if (selectedValue === undefined) return;

    if (isLastQuestion) {
      submitQuiz();
    } else {
      setCurrentIndex((i) => i + 1);
    }
  };

  // Basic keyboard support: number keys 1-4 pick an option, Enter advances.
  useEffect(() => {
    if (!currentQuestion || submitting) return;

    const handleKeyDown = (event) => {
      if (["1", "2", "3", "4"].includes(event.key)) {
        const idx = Number(event.key) - 1;
        const option = currentQuestion.options[idx];
        if (option) handleSelect(option.value);
      } else if (event.key === "Enter" && selectedValue !== undefined) {
        goNext();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentQuestion, selectedValue, submitting]);

  if (submitting) {
    return <LoadingScreen />;
  }

  if (loadingQuestions) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-ink-soft font-medium">Getting things ready...</p>
      </div>
    );
  }

  if (loadError || questions.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
        <AlertCircle className="text-rose-500 mb-3" size={32} />
        <p className="text-ink font-semibold mb-1">
          Couldn't read your mood right now. Try again.
        </p>
        <p className="text-ink-muted text-sm mb-6">
          Make sure the backend server is running.
        </p>
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="px-6 py-2.5 rounded-full bg-gradient-to-r from-rose-500 to-lavender-400 text-white font-semibold"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-16">
      <div className="w-full max-w-md">
        <div className="glass-card rounded-[2rem] px-6 sm:px-8 py-8">
          <div className="mb-8">
            <ProgressBar current={currentIndex + 1} total={questions.length} />
          </div>

          <div role="radiogroup" aria-label={currentQuestion.text}>
            <QuestionCard
              question={currentQuestion}
              selectedValue={selectedValue}
              onSelect={handleSelect}
            />
          </div>

          {submitError && (
            <p className="mt-4 text-sm text-rose-600 flex items-center gap-1.5">
              <AlertCircle size={14} /> {submitError}
            </p>
          )}

          <div className="flex items-center justify-between mt-8">
            <button
              type="button"
              onClick={goBack}
              className="inline-flex items-center gap-1 text-ink-soft font-medium px-4 py-2.5 rounded-full hover:bg-white/60 transition-colors"
            >
              <ChevronLeft size={18} />
              Back
            </button>

            <button
              type="button"
              onClick={goNext}
              disabled={selectedValue === undefined}
              className="inline-flex items-center gap-1 bg-gradient-to-r from-rose-500 to-lavender-400 text-white font-semibold px-6 py-2.5 rounded-full shadow-soft disabled:opacity-40 disabled:cursor-not-allowed enabled:hover:-translate-y-0.5 transition-all duration-200"
            >
              {isLastQuestion ? "See My Mood" : "Next"}
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
