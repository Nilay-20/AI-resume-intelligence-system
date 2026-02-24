import { useState } from "react";
import API from "../api/api";

function UploadResumes({ jobId }) {

  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const uploadFiles = async () => {

    if (!jobId) {
      alert("Create a job first");
      return;
    }

    if (files.length === 0) {
      alert("Select resumes");
      return;
    }

    const formData = new FormData();

    formData.append("job_id", jobId);

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      setUploading(true);

      const response = await API.post(
        "/files/upload-resumes",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("Upload successful");

      console.log(response.data);

    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ marginTop: "30px" }}>

      <h3>Upload Resumes</h3>

      <input
        type="file"
        multiple
        accept=".pdf"
        classname="border p-3 rounded w-full"
        onChange={handleFileChange}
      />

      <br /><br />

      <button className="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium hover:bg-blue-700 transition" onClick={uploadFiles}>
        {uploading ? "Uploading..." : "Upload Resumes"}
      </button>

    </div>
  );
}

export default UploadResumes;