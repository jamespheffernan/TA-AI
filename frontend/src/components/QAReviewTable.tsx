import React, { useState } from 'react';

interface QAReviewItem {
  id: number;
  question: string;
  answer: string;
  timestamp: string;
  flagged: boolean;
  feedback?: string;
}

interface QAReviewTableProps {
  items: QAReviewItem[];
}

export default function QAReviewTable({ items }: QAReviewTableProps) {
  const [data, setData] = useState<QAReviewItem[]>(items);

  const toggleFlag = (id: number) => {
    setData((prev) =>
      prev.map((item) => (item.id === id ? { ...item, flagged: !item.flagged } : item))
    );
  };

  const submitFeedback = (id: number, feedback: string) => {
    console.log(`Submit feedback for ${id}:`, feedback);
    setData((prev) =>
      prev.map((item) => (item.id === id ? { ...item, feedback } : item))
    );
  };

  return (
    <table className="min-w-full bg-white">
      <thead>
        <tr>
          <th className="p-2 text-left">Time</th>
          <th className="p-2 text-left">Question</th>
          <th className="p-2 text-left">Answer</th>
          <th className="p-2 text-left">Flagged</th>
          <th className="p-2 text-left">Feedback</th>
          <th className="p-2 text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id} className="border-b">
            <td className="p-2 text-sm">{new Date(item.timestamp).toLocaleString()}</td>
            <td className="p-2 text-sm">{item.question}</td>
            <td className="p-2 text-sm">{item.answer}</td>
            <td className="p-2 text-sm">{item.flagged ? '🚩' : ''}</td>
            <td className="p-2 text-sm">
              <input
                type="text"
                defaultValue={item.feedback || ''}
                className="border px-1 py-0.5 rounded w-full"
                onBlur={(e) => submitFeedback(item.id, e.target.value)}
              />
            </td>
            <td className="p-2 text-sm">
              <button
                onClick={() => toggleFlag(item.id)}
                className="text-blue-600 hover:underline"
              >
                {item.flagged ? 'Unflag' : 'Flag'}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}