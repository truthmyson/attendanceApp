// src/pages/ChangeReference.jsx
import { useState } from 'react';
import '../styles/ChangeReference.css';
import { FaSpinner, FaUpload } from 'react-icons/fa';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3636';

const ChangeReference = () => {
  const [colToDrop, setColToDrop] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    console.log('File selected:', selectedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setResponse({ success: false, message: 'Please select a file.' });
      return;
    }

    setLoading(true);
    setResponse(null);

    // Read file as base64
    const reader = new FileReader();
    reader.onload = async () => {
      try {
        // Remove the data URL prefix (e.g., "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,")
        const base64File = reader.result.split(',')[1];

        const payload = {
          ref_exe: base64File,
          col_to_drop: colToDrop.split(',').map(s => s.trim()).filter(s => s)
        };

        console.log('Payload prepared, sending to API...');

        const res = await fetch(`${API_BASE}/reference-excel`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        console.log('API response:', data);

        if (data.status === 'success') {
          setResponse({ success: true, message: data.message });
        } else {
          setResponse({ success: false, message: data.message || 'An error occurred.' });
        }
      } catch (error) {
        console.error('Error in handleSubmit:', error);
        setResponse({ success: false, message: 'Network error. Please try again.' });
      } finally {
        setLoading(false);
      }
    };

    reader.onerror = (error) => {
      console.error('FileReader error:', error);
      setResponse({ success: false, message: 'Failed to read file.' });
      setLoading(false);
    };

    reader.readAsDataURL(file);
  };

  return (
    <div className="change-reference">
      <h1>Update Reference Data</h1>
      <p>Upload an Excel file with reference information (e.g., holiday list, employee master).</p>

      <form onSubmit={handleSubmit} className="reference-form">
        <div className="form-group">
          <label>Columns to Drop (comma separated)</label>
          <input
            type="text"
            value={colToDrop}
            onChange={(e) => setColToDrop(e.target.value)}
            placeholder="e.g. Notes, Comments"
          />
        </div>

        <div className="form-group file-input">
          <label>Reference Excel File (XLSX only)</label>
          <div className="file-upload">
            <input 
              type="file" 
              accept=".xlsx" 
              onChange={handleFileChange} 
              required 
              id="file-upload"
            />
            <label htmlFor="file-upload" className="file-upload-label">
              <FaUpload className="upload-icon" />
              <span>{file ? file.name : 'Choose file...'}</span>
            </label>
          </div>
        </div>

        <button type="submit" className="submit-btn" disabled={loading || !file}>
          {loading ? <><FaSpinner className="spinner" /> PROCESSING...</> : 'Upload Reference'}
        </button>

        {response && (
          <div className={`response-message ${response.success ? 'success' : 'error'}`}>
            {response.message}
          </div>
        )}
      </form>
    </div>
  );
};

export default ChangeReference;