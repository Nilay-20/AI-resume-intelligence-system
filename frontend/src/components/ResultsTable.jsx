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

      <button className="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium hover:bg-blue-700 transition" onClick={downloadCSV}> 
        Download CSV Report
      </button>

      <br /><br />

      <table classname="w-full border-collapse">

        <thead>
          <tr>
            <th classname="p-3 text-left">Rank</th>
            <th classname="p-3 text-left">Resume</th>
            <th classname="p-3 text-left">Final Score</th>
            <th classname="p-3 text-left">Status</th>
            <th classname="p-3 text-left">Best Section</th>
          </tr>
        </thead>

        <tbody>
          {results.map((res, index) => (
            <tr key={index} classname="border-t hover:bg-gray-50">
              <td>{index + 1}</td>
              <td>{res.resume}</td>
              <td>{res.final_score?.toFixed(3)}</td>
              <td>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium
                        ${res.status === "Shortlisted"
                          ? "bg-green-100 text-green-700"
                          : res.status === "Review"
                          ? "bg-yellow-100 text-yellow-700"
                          : "bg-red-100 text-red-700"
                        }
                      `}>
                        {res.status}
                      </span>
                    </td>
              <td>{res.best_section}</td>
            </tr>
          ))}
        </tbody>

      </table>

    </div>
  );
}

export default ResultsTable;