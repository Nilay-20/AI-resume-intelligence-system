import { useState } from "react";
import API from "../api/api";

function StartEvaluation({ jobId, setActiveJob }) {

  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);

  const startEvaluation = async () => {

    if (!jobId) {
      alert("Create job first");
      return;
    }

    if (!jd.trim()) {
      alert("Enter Job Description");
      return;
    }

    const formData = new FormData();

    formData.append("job_id", jobId);
    formData.append("job_description", jd);

    try {
      setLoading(true);

      const response = await API.post(
        "/evaluation/evaluate",
        formData
      );

      setActiveJob(response.data.job_id);

      alert("Evaluation Started");

    } catch (error) {
      console.error(error);
      alert("Failed to start evaluation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "30px" }}>

      <h3>Job Description</h3>

      <textarea
        rows="6"
        cols="60"
        placeholder="Paste Job Description..."
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />

      <br /><br />

      <button onClick={startEvaluation}>
        {loading ? "Starting..." : "Start Evaluation"}
      </button>

    </div>
  );
}

export default StartEvaluation;