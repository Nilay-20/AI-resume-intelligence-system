import { useEffect, useState } from "react";
import API from "../api/api";

function ProgressTracker({ jobId, setCompleted }) {

  const [status, setStatus] = useState("");
  const [progress, setProgress] = useState("");

  useEffect(() => {

    if (!jobId) return;

    const interval = setInterval(async () => {

      try {
        const response = await API.get(
          `/evaluation/status/${jobId}`
        );

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

    }, 3000); // every 3 seconds

    return () => clearInterval(interval);

  }, [jobId]);

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Evaluation Progress</h3>

      <p><b>Status:</b> {status}</p>
      <p>{progress}</p>
    </div>
  );
}

export default ProgressTracker;