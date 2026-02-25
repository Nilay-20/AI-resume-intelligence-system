import { useState } from "react";
import API from "../api/api";

function UploadResumes({ jobId, showToast }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setUploaded(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = Array.from(e.dataTransfer.files).filter(f => f.type === "application/pdf");
    if (dropped.length > 0) {
      setFiles(dropped);
      setUploaded(false);
    } else {
      showToast("Only PDF files are accepted", "error");
    }
  };

  const uploadFiles = async () => {
    if (!jobId) return showToast("Create a job first", "error");
    if (files.length === 0) return showToast("Select resumes first", "error");

    const formData = new FormData();
    formData.append("job_id", jobId);
    files.forEach(f => formData.append("files", f));

    try {
      setUploading(true);
      await API.post("/files/upload-resumes", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploaded(true);
      showToast(`${files.length} resume${files.length > 1 ? "s" : ""} uploaded`, "success");
    } catch (error) {
      console.error(error);
      showToast("Upload failed", "error");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-3">
      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-5 text-center transition-all cursor-pointer
          ${isDragging
            ? "border-blue-500 bg-blue-950/30"
            : uploaded
            ? "border-green-700 bg-green-950/20"
            : "border-gray-700 hover:border-gray-500"
          }`}
      >
        <input
          type="file"
          multiple
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
          id="fileInput"
        />
        <label htmlFor="fileInput" className="cursor-pointer block">
          {uploaded ? (
            <p className="text-xs text-green-400 font-bold">✓ {files.length} file{files.length > 1 ? "s" : ""} uploaded</p>
          ) : files.length > 0 ? (
            <p className="text-xs text-blue-400 font-bold">{files.length} file{files.length > 1 ? "s" : ""} selected</p>
          ) : (
            <>
              <p className="text-xs text-gray-400">Drop PDF resumes here</p>
              <p className="text-xs text-gray-600 mt-0.5">or click to browse</p>
            </>
          )}
        </label>
      </div>

      {/* File list */}
      {files.length > 0 && !uploaded && (
        <div className="space-y-1 max-h-24 overflow-y-auto">
          {files.map((f, i) => (
            <div key={i} className="flex items-center gap-2 text-xs text-gray-500 bg-gray-900 rounded px-2 py-1">
              <span className="text-red-500">PDF</span>
              <span className="truncate">{f.name}</span>
            </div>
          ))}
        </div>
      )}

      {/* Upload button */}
      {files.length > 0 && !uploaded && (
        <button
          onClick={uploadFiles}
          disabled={uploading}
          className={`w-full py-1.5 rounded text-xs font-bold uppercase tracking-widest transition-all border
            ${uploading
              ? "border-gray-700 text-gray-600 cursor-not-allowed"
              : "border-blue-600 text-blue-400 hover:bg-blue-600 hover:text-white"
            }`}
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-3 h-3 rounded-full border border-gray-500 border-t-transparent animate-spin" />
              Uploading...
            </span>
          ) : `Upload ${files.length} Resume${files.length > 1 ? "s" : ""}`}
        </button>
      )}
    </div>
  );
}

export default UploadResumes;