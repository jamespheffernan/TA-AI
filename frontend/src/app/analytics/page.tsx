"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AnalyticsOverview from '@/components/AnalyticsOverview';

interface AnalyticsOverviewData {
  totalQuestions: number;
  flaggedCount: number;
  mostAsked: { question: string; count: number }[];
}

export default function AnalyticsPage() {
  const [overview, setOverview] = useState<AnalyticsOverviewData | null>(null);

  useEffect(() => {
    axios.get('/api/analytics')
      .then((res) => setOverview(res.data.overview))
      .catch((err) => console.error('Error fetching analytics:', err));
  }, []);

  if (!overview) {
    return <p>Loading analytics...</p>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Analytics Views</h1>
      <AnalyticsOverview data={overview} />
      {/* Add charts and detailed reports here */}
    </div>
  );
}