import React, { useState, useEffect } from 'react';

const Feedback = ({ report }) => {
  const [feedbackSent, setFeedbackSent] = useState(false);

  // This is the key fix.
  // The useEffect hook will run whenever the 'report' object changes.
  // This means when a new search result comes in, we reset the feedback form.
  useEffect(() => {
    setFeedbackSent(false);
  }, [report]); // The [report] part tells the hook to watch for changes to the report prop.

  const handleFeedback = async (isCorrect) => {
    try {
      const payload = {
        scraped_text: report.summary,
        model_prediction: report.risk_level,
        is_correct: isCorrect,
      };

      await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      setFeedbackSent(true);
    } catch (error) {
      console.error("Failed to send feedback:", error);
    }
  };

  if (feedbackSent) {
    return <p><em>Thank you for your feedback!</em></p>;
  }

  return (
    <div style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '10px' }}>
      <p>Was this analysis correct?</p>
      <button onClick={() => handleFeedback(true)} style={{ marginRight: '10px' }}>
        👍 Correct
      </button>
      <button onClick={() => handleFeedback(false)}>
        👎 Incorrect
      </button>
    </div>
  );
};

export default Feedback;