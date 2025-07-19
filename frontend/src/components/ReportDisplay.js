import React from 'react';
import Feedback from './Feedback'; // We will use the Feedback component again

const ReportDisplay = ({ report }) => {
  const articles = report.articles || [];
  const overallRisk = report.overall_risk || 'N/A';

  const getFlagColor = (level) => {
    if (level === 'HIGH') return 'red';
    if (level === 'MEDIUM') return 'orange';
    return 'green';
  };
  
  const getFlagEmoji = (level) => {
    if (level === 'HIGH') return '🔴';
    if (level === 'MEDIUM') return '🟡';
    return '🟢';
  };

  if (articles.length === 0) {
    return <p>No articles found for this search.</p>;
  }

  return (
    <div className="report-display">
      {/* --- NEW: Overall Risk Section --- */}
      <div style={{ marginBottom: '20px', paddingBottom: '10px', borderBottom: '2px solid #333' }}>
        <h2>Overall Risk Assessment</h2>
        <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
          <span style={{ color: getFlagColor(overallRisk) }}>{overallRisk}</span>
        </p>
      </div>
      {/* --------------------------------- */}

      <h2>Article-Level Analysis</h2>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {articles.map((article, index) => (
          <li key={index} style={{ marginBottom: '15px', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span style={{ fontSize: '1.5rem', marginRight: '10px' }}>
                {getFlagEmoji(article.risk_level)}
              </span>
              <div>
                <a 
                  href={article.url} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  style={{ textDecoration: 'none', color: '#007bff', fontWeight: 'bold' }}
                >
                  {article.title}
                </a>
                <p style={{ margin: '5px 0 0 0', fontSize: '0.9rem', color: '#555' }}>
                  Risk: {article.risk_level} (Confidence: {(article.risk_score * 100).toFixed(1)}%)
                </p>
              </div>
            </div>
            {/* --- NEW: Add Feedback component for each article --- */}
            <Feedback report={{summary: article.title, risk_level: article.risk_level}} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReportDisplay;