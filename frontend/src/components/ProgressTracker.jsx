import { useEffect, useState } from "react";
import API from "../api/api";

const STAGES = [
  { key: "parsing",   label: "Parsing Resumes",       pct: 25 },
  { key: "ranking",   label: "Semantic Scoring",       pct: 50 },
  { key: "market",    label: "Market RAG Augmentation", pct: 75 },
  { key: "completed", label: "Evaluation Complete",    pct: 100 },
];

function ProgressTracker({ jobId, setCompleted }) {
  const [status, setStatus] = useState("");
  const [progress, setProgress] = useState("Initializing pipeline...");

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const response = await API.get(`/evaluation/status/${jobId}`);
        setStatus(response.data.status);
        setProgress(response.data.progress);

        if (response.data.status === "completed") {
          clearInterval(interval);
          setCompleted(true);
        }
        if (response.data.status === "failed") {
          clearInterval(interval);
        }
      } catch (err) {
        console.error(err);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [jobId]);

  const currentPct = STAGES.find(s => s.key === status)?.pct ?? 5;

  return (
    <div className="max-w-lg mx-auto space-y-8">

      {/* Header */}
      <div className="flex items-center gap-3">
        <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
        <p className="text-xs uppercase tracking-widest text-gray-400 font-bold">Evaluation Running</p>
      </div>

      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-xs text-gray-600 mb-2">
          <span>Progress</span>
          <span>{currentPct}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-1.5">
          <div
            className="bg-blue-500 h-1.5 rounded-full transition-all duration-700 ease-out"
            style={{ width: `${currentPct}%` }}
          />
        </div>
      </div>

      {/* Stage indicators */}
      <div className="space-y-2">
        {STAGES.map((stage) => {
          const stageIdx = STAGES.findIndex(s => s.key === status);
          const thisIdx = STAGES.findIndex(s => s.key === stage.key);
          const isDone = stageIdx > thisIdx;
          const isActive = stage.key === status;

          return (
            <div key={stage.key} className={`flex items-center gap-3 px-3 py-2 rounded transition-all
              ${isActive ? "bg-gray-800 border border-gray-700" : "opacity-40"}`}>
              <div className={`w-4 h-4 rounded-full border flex items-center justify-center flex-shrink-0 text-xs
                ${isDone ? "border-green-500 bg-green-500 text-white" :
                  isActive ? "border-blue-400" : "border-gray-700"}`}>
                {isDone ? "✓" : isActive ? <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" /> : ""}
              </div>
              <span className={`text-xs font-mono ${isActive ? "text-gray-200" : isDone ? "text-gray-500" : "text-gray-700"}`}>
                {stage.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Current message */}
      <p className="text-xs text-gray-500 font-mono">{progress}</p>
    </div>
  );
}

export default ProgressTracker;