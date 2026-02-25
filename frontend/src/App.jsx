import { useState } from "react";
import CreateJob from "./components/CreateJob";
import UploadResumes from "./components/UploadResumes";
import StartEvaluation from "./components/StartEvaluation";
import ProgressTracker from "./components/ProgressTracker";
import ResultsTable from "./components/ResultsTable";

function App() {
  const [jobId, setJobId] = useState(null);
  const [activeJob, setActiveJob] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = "info") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  // Step completion states
  const step1Done = !!jobId;
  const step2Done = false; // tracked inside UploadResumes via callback
  const step3Done = !!activeJob;

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-gray-100 font-mono overflow-hidden">

      {/* Header */}
      <header className="flex-shrink-0 border-b border-gray-800 px-8 py-4 flex items-center justify-between bg-gray-950">
        <div className="flex items-center gap-4">
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
          <span className="text-sm font-bold tracking-widest uppercase text-gray-100">
            AI Resume Intelligence
          </span>
        </div>
        <div className="flex items-center gap-2">
          {["Transformer", "RAG", "FastAPI"].map(tag => (
            <span key={tag} className="text-xs px-2 py-0.5 rounded border border-gray-700 text-gray-500 tracking-wide">
              {tag}
            </span>
          ))}
        </div>
      </header>

      {/* Toast */}
      {toast && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-2 rounded text-sm font-mono border transition-all
          ${toast.type === "error" ? "bg-red-950 border-red-700 text-red-300" :
            toast.type === "success" ? "bg-green-950 border-green-700 text-green-300" :
            "bg-blue-950 border-blue-700 text-blue-300"}`}>
          {toast.msg}
        </div>
      )}

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">

        {/* LEFT PANEL — Stepper */}
        <div className="w-[400px] flex-shrink-0 border-r border-gray-800 flex flex-col overflow-y-auto">
          <div className="p-6 flex flex-col gap-1">
            <p className="text-xs text-gray-600 uppercase tracking-widest mb-6">Workflow</p>

            {/* Step 1 */}
            <Step number={1} label="Initialize Session" done={step1Done} active={!step1Done}>
              <CreateJob setJobId={setJobId} showToast={showToast} />
              {jobId && (
                <div className="mt-3 flex items-center gap-2">
                  <span className="text-xs text-gray-500">JOB ID</span>
                  <code className="text-xs bg-gray-800 border border-gray-700 text-blue-400 px-2 py-0.5 rounded">
                    {jobId}
                  </code>
                </div>
              )}
            </Step>

            {/* Step 2 */}
            <Step number={2} label="Upload Resumes" done={false} active={!!jobId} locked={!jobId}>
              {jobId
                ? <UploadResumes jobId={jobId} showToast={showToast} />
                : <p className="text-xs text-gray-600">Complete step 1 first</p>
              }
            </Step>

            {/* Step 3 */}
            <Step number={3} label="Job Description & Evaluate" done={!!activeJob} active={!!jobId && !activeJob} locked={!jobId}>
              {jobId
                ? <StartEvaluation jobId={jobId} setActiveJob={setActiveJob} showToast={showToast} />
                : <p className="text-xs text-gray-600">Complete step 1 first</p>
              }
            </Step>
          </div>
        </div>

        {/* RIGHT PANEL — Dynamic Display */}
        <div className="flex-1 flex flex-col overflow-hidden">

          {/* Idle */}
          {!activeJob && !completed && (
            <div className="flex-1 flex flex-col items-center justify-center gap-6 px-12 text-center">
              <div className="w-16 h-16 rounded-xl border border-gray-700 flex items-center justify-center">
                <svg className="w-8 h-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p className="text-lg font-bold text-gray-300 tracking-tight">Semantic Resume Screening</p>
                <p className="text-sm text-gray-600 mt-1 max-w-md">
                  Initialize a job session, upload candidate resumes, and provide a job description to begin transformer-based evaluation with market RAG augmentation.
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3 mt-2 w-full max-w-sm">
                {[
                  { label: "Semantic Similarity", desc: "Section-level scoring" },
                  { label: "Market RAG", desc: "Real-world augmentation" },
                  { label: "Explainable AI", desc: "Ranked with reasoning" },
                ].map(item => (
                  <div key={item.label} className="border border-gray-800 rounded-lg p-3 text-left">
                    <p className="text-xs font-bold text-gray-400">{item.label}</p>
                    <p className="text-xs text-gray-600 mt-0.5">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Progress */}
          {activeJob && !completed && (
            <div className="flex-1 flex flex-col justify-center px-12">
              <ProgressTracker jobId={activeJob} setCompleted={setCompleted} />
            </div>
          )}

          {/* Results */}
          {completed && (
            <div className="flex-1 overflow-y-auto px-8 py-6">
              <ResultsTable jobId={activeJob} showToast={showToast} />
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

function Step({ number, label, done, active, locked, children }) {
  return (
    <div className={`relative pl-10 pb-8 border-l-2 last:border-l-transparent transition-all
      ${locked ? "border-gray-800" : done ? "border-blue-800" : active ? "border-blue-500" : "border-gray-700"}`}>

      {/* Circle */}
      <div className={`absolute -left-[13px] top-0 w-6 h-6 rounded-full border-2 flex items-center justify-center text-xs font-bold transition-all
        ${locked ? "border-gray-700 bg-gray-950 text-gray-700" :
          done ? "border-blue-500 bg-blue-500 text-white" :
          active ? "border-blue-400 bg-gray-950 text-blue-400" :
          "border-gray-600 bg-gray-950 text-gray-600"}`}>
        {done ? "✓" : number}
      </div>

      {/* Label */}
      <p className={`text-xs uppercase tracking-widest mb-3 font-bold transition-all
        ${locked ? "text-gray-700" : done ? "text-blue-400" : active ? "text-gray-200" : "text-gray-500"}`}>
        {label}
      </p>

      {/* Content */}
      <div className={locked ? "pointer-events-none opacity-30" : ""}>
        {children}
      </div>
    </div>
  );
}

export default App;