import { useEffect, useState } from "react";
import API from "../api/api";

function ResultsTable({ jobId }) {

  const [results, setResults] = useState([]);

  useEffect(() => {

    if (!jobId) return;

    const fetchResults = async () => {
      try {

        const response = await API.get(
          `/evaluation/results/${jobId}`
        );

        setResults(response.data.results);

      } catch (error) {
        console.error(error);
      }
    };

    fetchResults();

  }, [jobId]);


  // ⭐ CSV DOWNLOAD
  const downloadCSV = async () => {
    try {

      const response = await API.get(
        `/evaluation/download/${jobId}`,
        {
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      );

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "resume_ranking.csv");

      document.body.appendChild(link);
      link.click();
      link.remove();

    } catch (error) {
      console.error(error);
      alert("Download failed");
    }
  };

  return (
    <div style={{ marginTop: "40px" }}>

      <h2>Candidate Rankings</h2>

      <button onClick={downloadCSV}>
        Download CSV Report
      </button>

      <br /><br />

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>Rank</th>
            <th>Resume</th>
            <th>Final Score</th>
            <th>Status</th>
            <th>Best Section</th>
          </tr>
        </thead>

        <tbody>
          {results.map((res, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{res.resume}</td>
              <td>{res.final_score?.toFixed(3)}</td>
              <td>{res.status}</td>
              <td>{res.best_section}</td>
            </tr>
          ))}
        </tbody>

      </table>

    </div>
  );
}

export default ResultsTable;