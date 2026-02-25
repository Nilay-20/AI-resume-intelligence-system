import { useState } from "react";
import API from "../api/api";

function CreateJob({ setJobId, showToast }) {
  const [loading, setLoading] = useState(false);

  const createJob = async () => {
    try {
      setLoading(true);
      const response = await API.post("/job/create");
      setJobId(response.data.job_id);
      showToast("Job session initialized", "success");
    } catch (error) {
      console.error(error);
      showToast("Failed to create job", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={createJob}
      disabled={loading}
      className={`flex items-center gap-2 px-4 py-2 rounded border text-xs font-bold uppercase tracking-widest transition-all
        ${loading
          ? "border-gray-700 text-gray-600 cursor-not-allowed"
          : "border-blue-600 text-blue-400 hover:bg-blue-600 hover:text-white"
        }`}
    >
      {loading ? (
        <>
          <span className="w-3 h-3 rounded-full border border-gray-500 border-t-transparent animate-spin" />
          Initializing...
        </>
      ) : (
        <>
          <span className="text-base leading-none">+</span>
          New Hiring Session
        </>
      )}
    </button>
  );
}

export default CreateJob;