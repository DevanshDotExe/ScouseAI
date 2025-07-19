import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/dashboard-data');
        const result = await response.json();
        setData(result.pieChart || []);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const COLORS = {
    'LOW': '#00C49F',   // Green
    'MEDIUM': '#FFBB28', // Yellow/Orange
    'HIGH': '#FF8042',    // Red
  };

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (data.length === 0) {
    return <p>No feedback data available to display.</p>;
  }

  return (
    <div className="report-display" style={{ width: '100%', height: 400 }}>
      <h2>Risk Level Distribution (from User Feedback)</h2>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={150}
            fill="#8884d8"
            dataKey="value"
            nameKey="name"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Dashboard;