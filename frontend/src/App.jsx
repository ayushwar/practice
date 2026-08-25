import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Quiz from "./pages/Quiz.jsx";
import Result from "./pages/Result.jsx";
import MoodOrbs from "./components/MoodOrbs.jsx";

export default function App() {
  // Answers and result live here so they survive navigation between
  // /quiz and /result without needing a global state library.
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  return (
    <div className="relative min-h-screen w-full overflow-x-hidden">
      <MoodOrbs />
      <div className="relative z-10">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/quiz"
            element={
              <Quiz
                answers={answers}
                setAnswers={setAnswers}
                setResult={setResult}
              />
            }
          />
          <Route
            path="/result"
            element={
              <Result
                result={result}
                answers={answers}
                setAnswers={setAnswers}
                setResult={setResult}
              />
            }
          />
        </Routes>
      </div>
    </div>
  );
}
