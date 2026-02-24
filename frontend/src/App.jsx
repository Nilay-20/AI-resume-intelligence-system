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

  return (
    <div style={{ padding: "40px" }}>

      <h1>AI Resume Screening Dashboard</h1>

      <CreateJob setJobId={setJobId} />

      {jobId && (
        <>
          <p><b>Active Job:</b> {jobId}</p>

          <UploadResumes jobId={jobId} />

          <StartEvaluation
            jobId={jobId}
            setActiveJob={setActiveJob}
          />
        </>
      )}

      {activeJob && !completed && (
        <ProgressTracker
          jobId={activeJob}
          setCompleted={setCompleted}
        />
      )}

      {completed && (
        <>
          <h3>✅ Evaluation Completed</h3>
          <ResultsTable jobId={activeJob} />
        </>
      )}

    </div>
  );
}

export default App;