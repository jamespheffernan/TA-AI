import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Health {
  status: string;
  timestamp: string;
  environment: string;
}

export default function HealthDashboard() {
  const [health, setHealth] = useState<Health | null>(null);

  useEffect(() => {
    axios.get('/api/admin/health')
      .then(res => setHealth(res.data))
      .catch(err => console.error('Error fetching health:', err));
  }, []);

  if (!health) {
    return <p>Loading health metrics...</p>;
  }

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">System Health Dashboard</h2>
      <p>Status: {health.status}</p>
      <p>Timestamp: {new Date(health.timestamp).toLocaleString()}</p>
      <p>Environment: {health.environment}</p>
    </div>
  );
}