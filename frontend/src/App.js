import React, { useState } from 'react';
import './styles/App.css';
import SearchForm from './components/SearchForm';
import ReportDisplay from './components/ReportDisplay';
import Dashboard from './components/Dashboard'; // Import the new component

function App() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('search'); // 'search' or 'dashboard'

  const handleAnalysis = async (entityName) => {
    setLoading(true);
    setReport(null); // Clear previous report
    const response = await fetch(`http://localhost:8000/analyze?entity_name=${entityName}`, {
      method: 'POST',
    });
    const data = await response.json();
    setReport(data);
    setLoading(false);
  };

  const renderContent = () => {
    if (view === 'dashboard') {
      return <Dashboard />;
    }
    // Default to 'search' view
    return (
      <>
        <SearchForm onAnalyze={handleAnalysis} loading={loading} />
        {loading && <p>Analyzing... please wait.</p>}
        {report && <ReportDisplay report={report} />}
      </>
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%'}}>
          <div>
            <h1>ScouseAI</h1>
            <p style={{margin: 0}}>AI-Powered Due Diligence</p>
          </div>
          <nav>
            <button onClick={() => setView('search')} disabled={view === 'search'}>
              Search
            </button>
            <button onClick={() => setView('dashboard')} disabled={view === 'dashboard'}>
              Dashboard
            </button>
          </nav>
        </div>
      </header>
      <main>
        {renderContent()}
      </main>
    </div>
  );
}

export default App;