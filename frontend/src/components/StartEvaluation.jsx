import { useState } from "react";
import API from "../api/api";

function StartEvaluation({ jobId, setActiveJob, showToast }) {
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);

  const startEvaluation = async () => {
    if (!jobId) return showToast("Create a job session first", "error");
    if (!jd.trim()) return showToast("Job description is required", "error");

    const formData = new FormData();
    formData.append("job_id", jobId);
    formData.append("job_description", jd);

    try {
      setLoading(true);
      const response = await API.post("/evaluation/evaluate", formData);
      setActiveJob(response.data.job_id);
      showToast("Evaluation pipeline started", "success");
    } catch (error) {
      console.error(error);
      showToast("Failed to start evaluation", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="relative">
        <textarea
          rows={5}
          placeholder="Paste job description here..."
          value={jd}
          onChange={(e) => setJd(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-xs text-gray-300
            placeholder-gray-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500
            resize-none transition-all font-mono"
        />
        <span className="absolute bottom-2 right-2 text-xs text-gray-700">
          {jd.length} chars
        </span>
      </div>

      <button
        onClick={startEvaluation}
        disabled={loading || !jd.trim()}
        className={`w-full py-2 rounded border text-xs font-bold uppercase tracking-widest transition-all
          ${loading || !jd.trim()
            ? "border-gray-700 text-gray-600 cursor-not-allowed"
            : "border-blue-600 text-blue-400 hover:bg-blue-600 hover:text-white"
          }`}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="w-3 h-3 rounded-full border border-gray-500 border-t-transparent animate-spin" />
            Starting Pipeline...
          </span>
        ) : "Run Evaluation"}
      </button>
    </div>
  );
}

export default StartEvaluation;