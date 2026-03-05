import '../styles/Home.css';
import { FaGoogle, FaCalendarAlt, FaFileExcel, FaDownload } from 'react-icons/fa';

const Home = () => {
  return (
    <div className="home">
      <section className="hero">
        <h1>Attendance Report Generator</h1>
        <p className="subtitle">Convert Google Forms attendance data into beautiful Excel reports</p>
      </section>

      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <FaGoogle className="step-icon" />
            <h3>1. Connect Google Sheet</h3>
            <p>Paste the URL of your Google Sheet (collected via Google Forms).</p>
          </div>
          <div className="step">
            <FaCalendarAlt className="step-icon" />
            <h3>2. Select Date Range</h3>
            <p>Choose the start and end dates for attendance filtering.</p>
          </div>
          <div className="step">
            <FaFileExcel className="step-icon" />
            <h3>3. Generate Draft</h3>
            <p>Our engine processes the data and creates a structured report.</p>
          </div>
          <div className="step">
            <FaDownload className="step-icon" />
            <h3>4. Download Excel</h3>
            <p>Get a clean, standardized Excel file ready for analysis.</p>
          </div>
        </div>
      </section>

      <section className="benefits">
        <h2>Benefits</h2>
        <div className="benefits-grid">
          <div className="benefit-card">
            <h3>Efficiency</h3>
            <p>Automate manual data processing and save hours of work.</p>
          </div>
          <div className="benefit-card">
            <h3>Accuracy</h3>
            <p>Eliminate human errors with precise data extraction and calculation.</p>
          </div>
          <div className="benefit-card">
            <h3>Standardized Reporting</h3>
            <p>Get consistent reports every time, ready for management review.</p>
          </div>
        </div>
      </section>

      <section className="contact">
        <h2>Contact Us</h2>
        <p>Have questions? Reach out to our team.</p>
        <div className="contact-info">
          <p>📞 +91 1234567791</p>
          <p>✉️ info@example.com</p>
          <p>🌐 www.attendancereport.com</p>
        </div>
      </section>
    </div>
  );
};

export default Home;