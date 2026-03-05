// src/pages/GenerateReport.jsx
import { useState } from 'react';
import '../styles/GenerateReport.css';
import { FaSpinner } from 'react-icons/fa';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3636';

const GenerateReport = () => {
  const [formData, setFormData] = useState({
    downloaded_col: '',
    excel_sheetname: '',
    reference_col: '',
    col_to_drop: '',
    urls: '' // textarea, one URL per line
  });
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [unprocessedSheets, setUnprocessedSheets] = useState([]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setUnprocessedSheets([]);

    // Prepare payload
    const payload = {
      downloaded_col: formData.downloaded_col,
      excel_sheetname: formData.excel_sheetname,
      reference_col: formData.reference_col,
      col_to_drop: formData.col_to_drop.split(',').map(s => s.trim()).filter(s => s),
      urls: formData.urls.split('\n').map(s => s.trim()).filter(s => s)
    };

    try {
      const res = await fetch(`${API_BASE}/generate-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      // Check for worker errors at top level
      if (data.report_metadata && data.report_metadata.status === 'error') {
        setResponse({ success: false, message: data.report_metadata.message });
      } else if (data.download_urls_metadata && data.download_urls_metadata.status === 'error') {
        setResponse({ success: false, message: data.download_urls_metadata.message });
      } else if (data.status === 'error') {
        setResponse({ success: false, message: data.message });
      } else {
        // Success: display main message and any unprocessed sheets
        setResponse({ success: true, message: data.message });
        if (data.body && data.body.unprocessed_sheets) {
          setUnprocessedSheets(Object.values(data.body.unprocessed_sheets));
        }
      }
    } catch (error) {
      console.log(error)
      setResponse({ success: false, message: 'Network error. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generate-report">
      <h1>Generate Attendance Report</h1>
      <p>Fill in the details to create a new report from your Google Sheets.</p>

      <form onSubmit={handleSubmit} className="report-form">
        <div className="form-group">
          <label>Downloaded Column *</label>
          <input type="text" name="downloaded_col" value={formData.downloaded_col} onChange={handleChange} required placeholder="e.g. index number" />
        </div>

        <div className="form-group">
          <label>Excel Sheet Name *</label>
          <input type="text" name="excel_sheetname" value={formData.excel_sheetname} onChange={handleChange} required placeholder="e.g. low level programming" />
        </div>

        <div className="form-group">
          <label>Reference Column *</label>
          <input type="text" name="reference_col" value={formData.reference_col} onChange={handleChange} required placeholder="e.g. INDEX" />
        </div>

        <div className="form-group">
          <label>Columns to Drop (comma separated)</label>
          <input type="text" name="col_to_drop" value={formData.col_to_drop} onChange={handleChange} placeholder="e.g. first name, last name" />
        </div>

        <div className="form-group">
          <label>Google Sheet URLs (one per line) *</label>
          <textarea name="urls" value={formData.urls} onChange={handleChange} required rows="5" placeholder="https://docs.google.com/..."></textarea>
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? <><FaSpinner className="spinner" /> PROCESSING...</> : 'Generate Excel Report'}
        </button>

        {response && (
          <div className={`response-message ${response.success ? 'success' : 'error'}`}>
            {response.message}
          </div>
        )}

        {unprocessedSheets.length > 0 && (
          <div className="unprocessed-sheets">
            <h4>Some sheets could not be processed:</h4>
            <ul>
              {unprocessedSheets.map((sheet, idx) => (
                <li key={idx}>{sheet.message || 'Unknown error'}</li>
              ))}
            </ul>
          </div>
        )}
      </form>
    </div>
  );
};

export default GenerateReport;