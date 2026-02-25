import { useEffect, useState } from "react";
import API from "../api/api";

function ResultsTable({ jobId, showToast }) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!jobId) return;

    const fetchResults = async () => {
      try {
        const response = await API.get(`/evaluation/results/${jobId}`);
        setResults(response.data.results);
      } catch (error) {
        console.error("Error fetching results:", error);
        showToast("Failed to load results", "error");
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [jobId]);

  const downloadCSV = async () => {
    try {
      const response = await API.get(`/evaluation/download/${jobId}`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "resume_ranking.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();
      showToast("Report downloaded", "success");
    } catch (error) {
      console.error(error);
      showToast("Download failed", "error");
    }
  };

  const maxScore = results.length > 0 ? Math.max(...results.map(r => r.final_score || 0)) : 1;

  const statusConfig = {
    shortlisted: { cls: "border-green-700 text-green-400 bg-green-950/40", label: "Shortlisted" },
    review:      { cls: "border-yellow-700 text-yellow-400 bg-yellow-950/40", label: "Review" },
    rejected:    { cls: "border-red-800 text-red-400 bg-red-950/40", label: "Rejected" },
  };

  return (
    <div className="h-full flex flex-col gap-4">

      {/* Header row */}
      <div className="flex items-center justify-between flex-shrink-0">
        <div>
          <p className="text-xs uppercase tracking-widest text-gray-500 font-bold">Evaluation Complete</p>
          <p className="text-lg font-bold text-gray-100 mt-0.5">
            Candidate Rankings
            <span className="ml-2 text-sm text-gray-600 font-normal">({results.length} candidates)</span>
          </p>
        </div>
        <button
          onClick={downloadCSV}
          className="flex items-center gap-2 px-3 py-1.5 border border-gray-700 rounded text-xs font-bold
            uppercase tracking-widest text-gray-400 hover:border-blue-600 hover:text-blue-400 transition-all"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export CSV
        </button>
      </div>

      {/* Table */}
      <div className="flex-1 overflow-y-auto rounded-lg border border-gray-800">
        {loading ? (
          <div className="flex items-center justify-center h-full text-xs text-gray-600">Loading results...</div>
        ) : results.length === 0 ? (
          <div className="flex items-center justify-center h-full text-xs text-gray-600">No results found.</div>
        ) : (
          <table className="w-full text-xs font-mono">
            <thead className="sticky top-0 bg-gray-900 border-b border-gray-800 z-10">
              <tr>
                {["#", "Resume", "Score", "Visual", "Status", "Best Section"].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-gray-600 uppercase tracking-widest font-bold">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results.map((res, index) => {
                const statusKey = res.status?.toLowerCase();
                const statusStyle = statusConfig[statusKey] || { cls: "border-gray-700 text-gray-500 bg-gray-900", label: res.status };
                const scoreVal = res.final_score || 0;
                const barWidth = maxScore > 0 ? (scoreVal / maxScore) * 100 : 0;

                return (
                  <tr
                    key={index}
                    className="border-b border-gray-800/60 hover:bg-gray-800/40 transition-colors"
                  >
                    {/* Rank */}
                    <td className="px-4 py-3 text-gray-600">
                      {index === 0
                        ? <span className="text-yellow-500 font-bold">01</span>
                        : <span>{String(index + 1).padStart(2, "0")}</span>
                      }
                    </td>

                    {/* Resume name */}
                    <td className="px-4 py-3 text-gray-300 max-w-[180px]">
                      <span className="truncate block" title={res.resume}>{res.resume}</span>
                    </td>

                    {/* Score */}
                    <td className="px-4 py-3 text-blue-400 font-bold tabular-nums">
                      {scoreVal.toFixed(3)}
                    </td>

                    {/* Score bar */}
                    <td className="px-4 py-3 w-28">
                      <div className="w-full bg-gray-800 rounded-full h-1.5">
                        <div
                          className="bg-blue-500 h-1.5 rounded-full transition-all duration-500"
                          style={{ width: `${barWidth}%` }}
                        />
                      </div>
                    </td>

                    {/* Status */}
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded border text-xs font-bold uppercase tracking-wider ${statusStyle.cls}`}>
                        {statusStyle.label}
                      </span>
                    </td>

                    {/* Best section */}
                    <td className="px-4 py-3 text-gray-500 italic">
                      {res.best_section || "—"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default ResultsTable;