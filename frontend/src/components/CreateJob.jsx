import { useState } from "react";
import API from "../api/api";

function CreateJob({ setJobId }) {

  const [loading, setLoading] = useState(false);

  const createJob = async () => {
    try {
      setLoading(true);

      const response = await API.post("/job/create");

      const id = response.data.job_id;

      setJobId(id);

    } catch (error) {
      console.error(error);
      alert("Failed to create job");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <button className="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium hover:bg-blue-700 transition" onClick={createJob}>
        {loading ? "Creating..." : "Create Hiring Job"}
      </button>
    </div>
  );
}

export default CreateJob;