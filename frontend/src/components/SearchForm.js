import React, { useState } from 'react';

const SearchForm = ({ onAnalyze, loading }) => {
  const [entityName, setEntityName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyze(entityName);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={entityName}
        onChange={(e) => setEntityName(e.target.value)}
        placeholder="Enter company or person's name"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
    </form>
  );
};

export default SearchForm;