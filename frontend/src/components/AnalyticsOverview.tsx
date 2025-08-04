import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

interface AnalyticsOverviewProps {
  data: {
    totalQuestions: number;
    flaggedCount: number;
    mostAsked: { question: string; count: number }[];
  };
}

export default function AnalyticsOverview({ data }: AnalyticsOverviewProps) {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">Analytics Overview</h2>
      <div className="mb-4">
        <p>Total Questions Asked: {data.totalQuestions}</p>
        <p>Flagged Answers: {data.flaggedCount}</p>
      </div>
      <div>
        <h3 className="font-medium mb-2">Most Asked Questions</h3>
        <ol className="list-decimal list-inside">
          {data.mostAsked.map((item, idx) => (
            <li key={idx}>
              {item.question} ({item.count})
            </li>
          ))}
        </ol>
      </div>
      <div className="mt-6">
        <h3 className="font-medium mb-2">Most Asked Questions Chart</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.mostAsked}>
            <XAxis dataKey="question" tick={{ fontSize: 12 }} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#4F46E5" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}