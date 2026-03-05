// src/pages/GetReport.jsx
import { useState } from 'react';
import '../styles/GetReport.css';
import { FaSpinner, FaDownload, FaSyncAlt, FaFileExcel } from 'react-icons/fa';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3636';

const GetReport = () => {
  const [filename, setFilename] = useState(null);
  const [loadingInfo, setLoadingInfo] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReportInfo = async () => {
    setLoadingInfo(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/report_info`);
      const data = await res.json();
      if (data.status === 'success') {
        setFilename(data.body.filename);
      } else {
        setError(data.message || 'Failed to fetch report info.');
      }
    } catch (err) {
      console.log(err)
      setError('Network error. Please try again.');
    } finally {
      setLoadingInfo(false);
    }
  };

  const handleDownload = async () => {
    setDownloading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/get_report_path`);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Error ${response.status}: ${response.statusText}`);
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      // Use the filename from state if available, else extract from header
      let downloadFilename = filename || 'report.xlsx';
      const contentDisposition = response.headers.get('Content-Disposition');
      if (contentDisposition) {
        const match = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
        if (match && match[1]) {
          downloadFilename = match[1].replace(/['"]/g, '');
        }
      }
      link.download = downloadFilename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="get-report">
      <h1>Retrieve Generated Report</h1>
      <p>Load the latest report information, then download.</p>

      <div className="actions">
        <button onClick={fetchReportInfo} className="info-btn" disabled={loadingInfo}>
          {loadingInfo ? <><FaSpinner className="spinner" /> LOADING...</> : 'Load Report Info'}
        </button>
        <button onClick={fetchReportInfo} className="reload-btn" title="Refresh" disabled={loadingInfo}>
          <FaSyncAlt />
        </button>
      </div>

      {filename && (
        <div className="report-info">
          <FaFileExcel className="excel-icon" />
          <span className="filename">{filename}</span>
          <button onClick={handleDownload} className="download-btn" disabled={downloading}>
            {downloading ? <><FaSpinner className="spinner" /> DOWNLOADING...</> : <><FaDownload /> Download</>}
          </button>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default GetReport;