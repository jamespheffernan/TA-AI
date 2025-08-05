import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend } from 'recharts';

interface AnalyticsOverviewProps {
  data: {
    totalQuestions: number;
    flaggedCount: number;
    mostAsked: { question: string; count: number }[];
  };
}

export default function AnalyticsOverview({ data }: AnalyticsOverviewProps) {
  const flaggedData = [
    { name: 'Flagged', value: data.flaggedCount },
    { name: 'Unflagged', value: data.totalQuestions - data.flaggedCount },
  ];
  const COLORS = ['#DC2626', '#10B981'];
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
      <div className="mt-6">
        <h3 className="font-medium mb-2">Flagged Answers Proportion</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={flaggedData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={80}
              label
            >
              {flaggedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}