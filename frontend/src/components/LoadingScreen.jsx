import { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";

const MESSAGES = [
  "Reading today's vibes...",
  "Looking at your answers...",
  "Checking your energy...",
  "Reading your social battery...",
  "Almost got it...",
];

export default function LoadingScreen() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % MESSAGES.length);
    }, 380);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
      <div className="relative h-20 w-20 mb-6">
        <div className="absolute inset-0 rounded-blob bg-gradient-to-br from-rose-400 via-lavender-400 to-peach-400 animate-pulse-soft blur-md" />
        <div className="absolute inset-0 flex items-center justify-center">
          <Sparkles className="text-white animate-drift" size={30} />
        </div>
      </div>
      <p className="font-display text-xl text-ink transition-opacity duration-300">
        {MESSAGES[index]}
      </p>
    </div>
  );
}
