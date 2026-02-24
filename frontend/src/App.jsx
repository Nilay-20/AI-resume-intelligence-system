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
    <div className="min-h-screen bg-gray-100">

      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto p-6">
          <h1 className="text-3xl font-bold">
            AI Resume Screening Dashboard
          </h1>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto p-8 space-y-6">

        <Card>
          <CreateJob setJobId={setJobId}/>
        </Card>

        {jobId && (
          <>
            <Card>
              <p className="font-medium">
                Active Job:
                <span className="ml-2 text-blue-600">
                  {jobId}
                </span>
              </p>
            </Card>

            <Card>
              <UploadResumes jobId={jobId}/>
            </Card>

            <Card>
              <StartEvaluation
                jobId={jobId}
                setActiveJob={setActiveJob}
              />
            </Card>
          </>
        )}

        {activeJob && !completed && (
          <Card>
            <ProgressTracker
              jobId={activeJob}
              setCompleted={setCompleted}
            />
          </Card>
        )}

        {completed && (
          <Card>
            <ResultsTable jobId={activeJob}/>
          </Card>
        )}

      </div>
    </div>
  );
}

function Card({ children }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      {children}
    </div>
  );
}

export default App;